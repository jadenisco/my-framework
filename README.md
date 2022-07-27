# my-framework

Experiment with VPP test framework

The Makefile output:
``` console

rm -rf /venv
mkdir -p /venv/run
python3 -m venv /venv
# pip version pinning
bash -c "source /venv/bin/activate && \
	  python3 -m pip install pip===22.0.4"
bash -c "source /venv/bin/activate && \
	  python3 -m pip install pip-tools===6.6.0"
bash -c "source /venv/bin/activate && \
	  python3 -m pip install setuptools===62.1.0"
touch /venv/run/pip-tools-install-3-6.6.0.done
bash -c "source /venv/bin/activate && \
	  python3 -m piptools sync requirements-3.txt"
touch /venv/run/pip-install-3-22.0.4.done
find: ‘/venv/lib/python*’: No such file or directory
echo --- patching ---
sleep 1 # Ensure python recompiles patched *.py files -> *.pyc
for f in /home/jdenisco/vpp-latest/test/patches/scapy-2.4.3/*.patch ; do \
	echo Applying patch: $(basename $f) ; \
	patch --forward -p1 -d  < $f ; \
	retCode=$?; \
	[ $retCode -gt 1 ] && exit $retCode; \
done; \
touch /venv/run/pip-patch-3.done
bash -c "source /venv/bin/activate && python3 -m pip install -e /src/vpp-api/python"
touch /venv/run/papi-install-3.done
rm -f /dev/shm/vpp-unittest-*
if [ 0 -eq "0" ] ; then rm -rf /tmp/vpp-unittest-*;  fi
rm -f /tmp/api_post_mortem.*
rm -rf /tmp/vpp-failed-unittests/
mkdir -p /tmp/vpp-failed-unittests/
bash -c "test 0 -eq 0 ||\
    (echo \"*******************************************************************\" &&\
	 echo \"* Sanity check failed, TEST_JOBS is not 1 or 'auto' and DEBUG, STEP or PROFILE is set\" &&\
         echo \"*******************************************************************\" &&\
	 false)"
bash -c "source /venv/bin/activate && python3 sanity_import_vpp_papi.py ||\
	(echo \"*******************************************************************\" &&\
	 echo \"* Sanity check failed, cannot import vpp_papi\" &&\
	 echo \"* to debug: \" &&\
	 echo \"* 1. enter test shell:   make test-shell\" &&\
	 echo \"* 2. execute debugger:   gdb python -ex 'run sanity_import_vpp_papi.py'\" &&\
         echo \"*******************************************************************\" &&\
	 false)"
echo "In the test dir, the test function"
echo "The RETEST FUNC"
scripts/run.sh --python-opts= --failed-dir=/tmp/vpp-failed-unittests/ --verbose=0 --jobs=1 --filter= --retries= --venv-dir=/venv --vpp-ws-dir= --vpp-tag= --rnd-seed= --vpp-worker-count="" --keep-pcaps   --sanity            --cache-vpp-output     || env FAILED_DIR=/tmp/vpp-failed-unittests/ COMPRESS_FAILED_TEST_LOGS= scripts/compress_failed.sh
```

run.sh:
``` console

#!/bin/bash

ff="0"
items=
for i in "$@"
do
case $i in
	--venv-dir=*)
		venv_dir="${i#*=}"
		if [ -d $venv_dir ]
		then
			venv_dir=$(cd $venv_dir; pwd)
		else
			echo "ERROR: '$venv_dir' is not a directory"
			exit 1
		fi
		items="$items --venv-dir=\"$venv_dir\""
		;;
	--vpp-ws-dir=*)
		ws_dir="${i#*=}"
		if [ -d $ws_dir ]
		then
			ws_dir=$(cd $ws_dir; pwd)
		else
			echo "ERROR: '$ws_dir' is not a directory"
			exit 1
		fi
		items="$items --vpp-ws-dir=\"$ws_dir\""
		;;
	--force-foreground)
		ff="1"
		items="$items \"$i\""
		;;
	--vpp-tag=*)
		tag="${i#*=}"
		items="$items \"$i\""
		;;
	--python-opts=*)
		python_opts="${i#*=}"
		;;
	*)
		# unknown option - skip
		items="$items \"$i\""
		;;
esac
done

extra_args=""
if [ -z "$ws_dir" ]
then
	ws_dir=$(pwd)
	echo "Argument --vpp-ws-dir not specified, defaulting to '$ws_dir'"
	extra_args="$extra_args --vpp-ws-dir=$ws_dir"
fi

if [ -z "$venv_dir" ]
then
	venv_dir="$ws_dir/test/venv"
	echo "Argument --venv-path not specified, defaulting to '$venv_dir'"
	extra_args="$extra_args --venv-dir=$venv_dir"
fi

if [ -z "$tag" ]
then
	tag="vpp_debug"
	echo "Argument --vpp-tag not specified, defaulting to '$tag'"
	extra_args="$extra_args --vpp-tag=$tag"
fi

eval set -- $items
$ws_dir/test/scripts/setsid_wrapper.sh $ws_dir/test/scripts/run_in_venv_with_cleanup.sh $ff $venv_dir/bin/activate python3 $python_opts $ws_dir/test/run_tests.py $extra_args $*


```