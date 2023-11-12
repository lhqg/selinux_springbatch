#!/bin/bash
#################################################################
# Springboot batch job control script.
#
# This is called by systemmd to start the batch job
#
# It is also used to perform pre-start checks, post-start checks
#   and cleanup operations.
#
# restart/reload operations will be perfomed calling systemctl
#
# Usage:
# ./springbatch-service.sh Springboot_JobName stop|start|restart|status
#
##################################################################

function usage {
	echo "Usage: $0 springboot-JobName {start|precheck|postcheck|cleanup|restart|reload}"
}

springbatch_ROOT=/opt/springbatch
springbatch_LOGROOT=/var/log/springbatch

if [ $# -eq 2 ]
then
	PATH=/usr/bin:/usr/sbin:/bin:/sbin:$PATH

	JOB_NAME="$1"

	JOB_BASE="${springbatch_ROOT}/${JOB_NAME}"
	JOB_LOGDIR="${springbatch_LOGROOT}/${JOB_NAME}"

	#
	# Check environment (as set by SystemD)
	#

	if echo "${JOB_NAME}" | egrep -q '&|;|>|<' ; then
		echo "FATAL: The job name contains forbidden characters."
		exit 127
	fi

	if [ -z "${JAVA_HOME}" ]
	then
		echo "FATAL: JAVA_HOME is not set."
		exit 127
	fi

	if [ -z "${JOB_JAR_FILEPATH}" ]
	then
		echo "FATAL: JOB_JAR_FILEPATH is not set."
		exit 127
	fi

	if [ -z "${LOG_PATH}" ]
	then
		echo "FATAL: LOG_PATH is not set."
		exit 127
	fi

	if [ -z "${LOADER_PATH}" ]
	then
		echo "FATAL: LOADER_PATH is not set."
		exit 127
	fi

	if [ -z "${JAVA_TMPDIR}" ]
	then
		echo "FATAL: JAVA_TMPDIR is not set."
		exit 127
	fi

	if [ -z "${JVM_MEM_OPTS}" ]
	then
		echo "FATAL: JVM_MEM_OPTS is not set."
		exit 127
	fi

	if [ -z "${JAVA_SECURITY_FILE}" ]
	then
		echo "FATAL: JAVA_SECURITY_FILE is not set."
		exit 127
	fi


	#
	# Declare functions
	#

	# Returns PID of Springboot batch job Java process
	function get_pid {
		regex_escaped_JOB_NAME=$(sed -r 's/([\x5d.+?*:{}\[])/\\\1/g' <<< "$JOB_NAME")
		pgrep -f "^([^/]*/)*java\s+(.*?\s+)?-DJOB_NAME=${regex_escaped_JOB_NAME}(\s|$)"
	}

	# Cleanup the job temporary files directory
	function cleanup {
		if [ -d "${JAVA_TMPDIR}" ]
		then
			find "${JAVA_TMPDIR}" -type f -mtime +10 -print0 | xargs -r -0 rm -f
			find "${JAVA_TMPDIR}" -mindepth 2 -type d -empty -print0 | xargs -r -0 rmdir
			find "${JAVA_TMPDIR}" -mindepth 1 -type d \! -name 'dynlib' -empty -print0 | xargs -r -0 rmdir 
		fi

		return 0
	}

	# Performs sanity checks before starting the Springboot batch job,
	function precheck {
		job_PID=$(get_pid)

		if [[ "$job_PID" != "" ]]; then
			echo "Job appears to still be running with PID $job_PID. Precheck failed."
			return 2
		fi

		if [[ ! -d "${JAVA_HOME}" ]] ; then
			echo "The JAVA_HOME variable points to non existent directory. Precheck failed."
			return 2
		fi

		if [[ ! -d "${JAVA_TMPDIR}" ]] ; then
			echo "The JAVA_TMPDIR variable points to non existent directory. Precheck failed."
			return 2
		fi

		if [[ ! -r "${JOB_JAR_FILEPATH}" ]] ; then
			echo "The JOB_JAR_FILEPATH variable points to non existent file. Precheck failed."
			return 2
		fi

		if echo "${JVM_MEM_OPTS}" | egrep -q '&|;|>|<' ; then
			echo "The JVM_MEM_OPTS variable contains forbidden characters. Precheck failed."
			return 3
		fi

		if echo "${JAVA_EXTRA_ARGS}" | egrep -q '&|;|>|<' ; then
			echo "The JAVA_EXTRA_ARGS variable contains forbidden characters. Precheck failed."
			return 3
		fi

		if echo "${JAR_OPTS}" | egrep -q '&|;|>|<' ; then
			echo "The JAR_OPTS variable contains forbidden characters. Precheck failed."
			return 3
		fi

		if [[ -n "${SPRING_CONFIG_LOCATION}" && ! -r "${SPRING_CONFIG_LOCATION}" ]] ; then
			echo "The SPRING_CONFIG_LOCATION variable points to non existent file. Precheck failed."
			return 3
		fi

		echo "Environment seems OK. Precheck succeeded."
		return 0
	}

	# Starts the Springboot batch job
	function start {
		declare -i my_PPID
		my_PPID=$( ps --no-headers -o ppid $$ )

		if [[ "$my_PPID" != "1" ]]; then
			echo "FATAL: Springboot batch job can only be started using systemd. Start aborted."
			return 127
		else

			echo "INFO: Staring Java process for Springboot batch job ${JOB_NAME}."
			echo "INFO:	Using JAVA_HOME: $JAVA_HOME"
			echo "INFO:	Using Java tmpdir: $JAVA_TMPDIR"
			echo "INFO:	Using Java Security file: $JAVA_SECURITY_FILE"

			if [[ -n "${SPRING_CONFIG_LOCATION}" ]] ; then
				echo "INFO:	Using Spring config file: $SPRING_CONFIG_LOCATION"
				SPRING_CONFIG_OPT="-Dspring.config.location=file:${SPRING_CONFIG_LOCATION}"
			else
				SPRING_CONFIG_OPT=""
			fi

			trap "" SIGHUP
			$JAVA_HOME/bin/java -DJOB_NAME="${JOB_NAME}" \
				${JVM_MEM_OPTS} \
				-Dloader.path="${LOADER_PATH}" \
				-DLOG_PATH="${LOG_PATH}" \
				-Djava.io.tmpdir=${JAVA_TMPDIR} \
				-Djava.security.properties=${JAVA_SECURITY_FILE} \
				${SPRING_CONFIG_OPT} \
				${JAVA_EXTRA_ARGS} \
				-jar "${JOB_JAR_FILEPATH}" ${JAR_OPTS} &

			jobpid=$!
			sleep 1
			ps ${jobpid} >/dev/null 2>&1
			if [[ $? == 0 ]] ; then
				return 0
			else
				echo "FATAL: Java process for Springboot batch job ${JOB_NAME} died prematurely."
				return 10
			fi
		fi
	}


	#
	# Main
	#

	case "$2" in
		cleanup)
			cleanup
			RC=$?
		;;
		precheck)
			precheck
			RC=$?
		;;
		start)
			start
			RC=$?
		;;
		restart|reload)
			/usr/bin/systemctl restart springbatch@${JOB_NAME}.service
			RC=$?
		;;
		status)
			/usr/bin/systemctl status springbatch@${JOB_NAME}.service
			RC=$?
		;;
		*)
			usage
			echo "Unknown option [$2]"
			RC=1
	esac

else
	usage
	RC=1
fi

exit $RC
