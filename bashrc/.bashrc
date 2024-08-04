# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

LS_COLORS='di=1;34:fi=0:ln=31:pi=5:so=5:bd=1;34:cd=5:or=31:mi=0:ex=35:ow=1;34'

#==============================================================================
# For fedora 36
#==============================================================================
alias open="xdg-open"
alias o="xdg-open"
alias gnome-open="xdg-open"
alias edit="pluma"
alias p="pluma"
alias e="emacs"
alias m="make"
alias t="x-tile g 3 3"
alias t2="x-tile g 2 2"
alias t3="x-tile g 3 3"
alias ex="exit;exit;exit"

function update_vm() { cwd=$(pwd); cd /home/student; rm -rf update-vm; git clone http://github.com/yliow/update-vm; cd update-vm; python update $@; cd "${cwd}";};
#function update_vm() { printf "Login as root and execute update-vm if update-vm is installed. To install update-vm, execute\n  su\n  cd /home/student\n  git clone http://github.com/yliow/update-vm\n  cd update-vm\n  python update\n";}
alias update-vm='update_vm'
    
alias alex='python ~/.alex/alexrunner.py'

export EDITOR='emacs'
umask 077
