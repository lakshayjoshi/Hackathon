As root:

#Add users
useradd -m hero
useradd -m secretuser

#Set passwords for newly created users
echo "hero:action123" | chpasswd
echo "secretuser:secretpassword" | chpasswd

#Establish secretuser_pass/secretuser file and set its permissions
mkdir -p /etc/secretuser_pass
echo "CTFEYDSCI{pr1v173ge_35c4l4tion_p455}" > /etc/secretuser_pass/secretuser
chmod 600 /etc/secretuser_pass/secretuser
chown secretuser:secretuser /etc/secretuser_pass/secretuser

#save a new file as actionreplay.c in /home/hero/

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    int c;               /* IMPORTANT: int, not char */

    fp = fopen("/tmp/file.log", "r");
    if (fp == NULL) {
        puts("Cannot find /tmp/file.log");
        return 1;
    }

    while ((c = fgetc(fp)) != EOF) {
        putchar(c);
    }

    fclose(fp);
    return 0;
}

#Compile the code into executable
gcc /home/hero/actionreplay.c -o /home/hero/actionreplay

#Now set ownership and permissions:
chown leviathan6:leviathan5 /home/leviathan5/leviathan5
chmod 4750 /home/leviathan5/leviathan5

#Ensure users cant read each others' home
chmod 750 /home/leviathan5
chmod 750 /home/leviathan6

#Check the kernel protection flags

# show current values
cat /proc/sys/fs/protected_symlinks
cat /proc/sys/fs/protected_hardlinks

(if either returns "1", code will not work)

#Run strace to see the actual error when binary tries to open
strace -e trace=open,openat -f ./actionreplay 2>&1 | sed -n '1,120p'

(You will likely see open("/tmp/file.log", O_RDONLY) = -1 EACCES (Permission denied) or another errno related to symlink protections)

#Turn symlink protection off and save this code in /etc/systcl.d/99-challenge.conf
fs.protected_symlinks=0
fs.protected_hardlinks=0

#Restart sysctl
sudo sysctl --system

#Verify
cat /proc/sys/fs/protected_symlinks
cat /proc/sys/fs/protected_hardlinks

(both should return 0 now)

#enable ssh on the server
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager(to check)

#disable ssh on the server
sudo systemctl disable --now ssh
systemctl status ssh --no-pager(to check)



