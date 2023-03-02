#!/usr/bin/env groovy
// This file is adapted from https://git.corp.adobe.com/euclid/python-project-scaffold
properties([
  buildDiscarder(logRotator(daysToKeepStr: '180', numToKeepStr: '900'))
])

// dn-console-mac-build-node is the tag for Jenkins node that should run the test.
// Additional info can be passed in this dictionary like config, but we won't use it now.
// Please be mindful of the limited resources on Jenkins when setting the timeout and issuing retries for jobs.
// If you need to replay a job on only one platform, please comment the other platforms out for the replay to conserve build resources
def profiles = [
  // [name:'mac-debug', label: 'dn-console-mac-build-node', config: 'Debug', timeout: '20', timeout_unit: 'MINUTES'],
  [name:'mac-release', label: 'dn-console-mac-build-node', config: 'Release', timeout: '10', timeout_unit: 'MINUTES'],
  // [name:'win-debug', label: 'dn-console-win-build-node', config: 'Debug', timeout: '20', timeout_unit: 'MINUTES'],
  [name:'win-release', label: 'dn-console-win-build-node', config: 'Release', timeout: '10', timeout_unit: 'MINUTES'],
  // [name:'ubuntu-debug',  label: 'dn-linux-build-node', config: 'Debug', timeout: '20', timeout_unit: 'MINUTES'],
  [name:'ubuntu-release',  label: 'dn-linux-build-node', config: 'Release', timeout: '10', timeout_unit: 'MINUTES'],
]

def build(profile) {
  node(profile.label) {
    timeout([time: profile.timeout, unit: profile.timeout_unit]) {
      withCredentials([
        // These are credentials available on Jenkins. This will make them available as env vars for build.
        sshUserPrivateKey(credentialsId: 'c4279c21-d85b-4493-afdf-2677507825b5', keyFileVariable: 'SSH_KEY_PATH', usernameVariable: 'eucbot'),
        usernamePassword(credentialsId: '4a3cae41-d419-427f-a9b7-2724755a3216', passwordVariable: 'ARTIFACTORY_API_KEY', usernameVariable: 'ARTIFACTORY_USERNAME')
      ]) {
        try {
          stage(profile.name) {
            deleteDir()
            checkout scm
            // alternately, if you want to run different commands on linux, you can check the profile.name
            // e.g. if (profile.name.startswith(ubuntu))
            if (isUnix()) {  // works for both linux and mac
              sh label: "Activate Conda", script: '''
                set +x
                # uncomment the following line for verbosity
                # it could be set with -v, -vv, -vvv
                # export CONDA_DEBUG_FLAG=-vvv
                . ./tools/setup.sh
              '''

              sh label: "Print ENV", script: '''
                set +x
                echo "--- node ${NODE_NAME} ---"
                env | sort
                echo "--- node ${NODE_NAME} ---"
              '''

              sh label: "Sync artifacts", script: '''
                set +x
                . .miniconda3/bin/activate
                conda activate .venv/
                python tools/artifacts.py pull
              '''

              // this is just a stub (python projects don't need to be configured)
              // sh label: "Make project", script: '''
              //   set +x
              //   . .miniconda3/bin/activate
              //   conda activate .venv/
              //   # if you have a C++ project, you can configure the build
              //   # here (e.g. build the vsproj, the xcodeproj, or run make)
              // '''

              sh label: "Build and test", script: """
                set +x
                . .miniconda3/bin/activate
                conda activate .venv/
                mkdir .tmp_test_out
                # if you need to access a build configuration (Release/Debug) you can get it from the profile.config variable
                python tests/main.py --xml=.tmp_test_out/test_report.xml --log=.tmp_test_out/${profile.name}_test_log.txt
              """
            } else {  // windows
              bat label: "Activate Conda", script: '''
                :: uncomment the following line for verbosity
                :: it could be set with -v, -vv, -vvv
                :: set CONDA_DEBUG_FLAG=-vvv
                powershell tools/setup.ps1
              '''

              bat label: "Print ENV", script: '''
                @echo --- node %NODE_NAME% ---
                set
                @echo --- node %NODE_NAME% ---
              '''

              bat label: "Sync artifacts", script: '''
                call .miniconda3/Scripts/activate.bat
                call activate .venv/
                python tools/artifacts.py pull
              '''

              // this is just a stub (python projects don't need to be configured)
              // bat label: "Make project", script: '''
              //   call .miniconda3/Scripts/activate.bat
              //   call activate .venv/
              //   # if you have a C++ project, you can configure the build
              //   # here (e.g. build the vsproj, the xcodeproj, or run make)
              // '''

              bat label: "Build and test", script: """
                call .miniconda3/Scripts/activate.bat
                call activate .venv/
                mkdir .tmp_test_out
                :: if you need to access a build configuration (Release/Debug) you can get it from the profile.config variable
                python tests/main.py --xml=.tmp_test_out/test_report.xml --log=.tmp_test_out/${profile.name}_test_log.txt
              """
            }
          }
        } finally {
          // this is where you can upload any build logs or images to artifactory if you want to
          archiveArtifacts artifacts: '.tmp_test_out/*_test_log.txt'
          junit testResults: '.tmp_test_out/test_report.xml'
        }
      }
    }
  }
}

// Cancel old jobs on the same branch
def buildNumber = BUILD_NUMBER as int;
if (buildNumber > 1) milestone(buildNumber - 1);
milestone(buildNumber)

timestamps {
  parallel profiles.collectEntries { profile ->
    [ "${profile.name}" : {
      build(profile)
    } ]
  }
}
