# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
	for rc in ~/.bashrc.d/*; do
		if [ -f "$rc" ]; then
			. "$rc"
		fi
	done
fi

unset rc


# From /home/student/.bashrc:
LS_COLORS='di=1;34:fi=0:ln=31:pi=5:so=5:bd=1;34:cd=5:or=31:mi=0:ex=35:ow=1;34'
alias open="xdg-open"
alias o="xdg-open"
alias gnome-open="xdg-open"
alias x="emacs"
alias m="make"
alias t="x-tile g 2 2"
alias t2="x-tile g 2 2"
alias t3="x-tile g 3 3"
alias ex="exit;exit;exit"

# For update-vm
function update_vm() { cwd=$(pwd); cd /home/student; rm -rf update-vm; git clone http://github.com/yliow/update-vm; cd update-vm; python update $@; cd "${cwd}";};
alias update-vm='update_vm'

