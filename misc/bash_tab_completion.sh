: ${TOMCAT_INSTANCES_DIR:=/usr/local/tomcat_instances}

_instance_manager() {
  COMPREPLY=()

  local verbs="manage start stop restart status enable disable"
  local man_tasks="start stop reload redeploy undeploy list deploy"
  
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"

  local action=${COMP_WORDS[1]}
  local instance=${COMP_WORDS[2]}
  
  local inst_list=$(find ${TOMCAT_INSTANCES_DIR} -mindepth 1     \
                    -maxdepth 1 -type d -regex '.+/[ABCDEFGHIJKLMNOPQRSTUVWXYZ].+' |   \
                    xargs -r -n1 basename)
                    # -regex [A-Z] is not case sensitive for me. don't understand why :-(

  local disabled_list=$(find ${TOMCAT_INSTANCES_DIR} -mindepth 1     \
                        -maxdepth 1 -type d -regex '.+/_[ABCDEFGHIJKLMNOPQRSTUVWXYZ].+' |   \
                        xargs -r -n1 basename | sed  's/^_//')
  

  case "$prev" in

    [ABCDEFGHIJKLMNOPQRSTUVWXYZ]*)
      case "$action" in 
        manage)
          COMPREPLY=( $(compgen -W "$man_tasks" -- "$cur") )
          ;;
        stop)
          #COMPREPLY=( $(compgen -W "force" -- "$cur") )
          COMPREPLY=''
          ;;
        *)
          COMPREPLY=''
          ;;
      esac
      return 0
      ;;

    manage)
      COMPREPLY=( $(compgen -W "$inst_list" -- "$cur") )
      return 0
      ;;

    start|stop|restart|disable)
      COMPREPLY=( $(compgen -W "$inst_list" -- "$cur") )
      ;;

    enable)
      COMPREPLY=( $(compgen -W "$disabled_list" -- "$cur") )
      ;;

    redeploy|undeploy|reload)
      webapps="$(find ${TOMCAT_INSTANCES_DIR}/$instance/conf/Catalina/localhost/ -type f | xargs -r -i -n1 basename '{}' .xml)"
      COMPREPLY=( $(compgen -W "$webapps" -- "$cur") )
      return 0
      ;;

    deploy)
      ;;

    status|list)
      COMPREPLY=''
      ;;

    *)
      COMPREPLY=($(compgen -W "$verbs" -- "$cur"))
      ;;
  esac
  
  return 0
}
# use default for clean filename completion, filename completion
# with 'compgen -f' looks like ass
complete -F "_instance_manager" -o default "instance_manager"
