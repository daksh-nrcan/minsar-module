# SSH


### SSH Client Setup

Nutshell: VSCode best imo, but download both 

- [MobaxTerm Download](https://mobaxterm.mobatek.net/download-home-edition.html): get home edition
- [VSCode Download](https://code.visualstudio.com/download): get extensions 'Remote - SSH' and 'Remote - SSH: Editing Configuration'



### Salish


Nutshell: Allows you to access leo2g from home

##### Creating SSH Key (Windows/MobaxTerm)

Create a new shell on the local work laptop, then:

```bash
cd /drives/c/<username>
mkdir .ssh && cd .ssh # if doesn't already exist

ssh-keygen -t ed25519 -C "leo2g/salish login" -f "id_salish"
```
Note: You can use the MobaxTerm MobaKeyGen tool, but it doesn't output in OpenSSH format which causes headaches later. Plus it basically just fills in the above fields.

Anyways, this will create two files:

- id_salish: PRIVATE key (no file extension)
- id_salish.pub: public key

Send the public key to `jiangheng.he@nrcan-rncan.gc.ca`

After, change the permissions on your SSH keys, this caused silent errors for me:

```bash
chmod 600 ~/.ssh/id_ed25519 # private key, only owner read/write
chmod 644 ~/.ssh/id_ed25519.pub # public key, easier
chmod 700 ~/.ssh/ # directory accessible by other users I think
```



### Configuring Laptop for SSH ProxyJump with Alias

There's two steps to 'SSH' into leo2g from home, via Salish, then Leo2g. This `~/.ssh/config` file abstracts everything:

```
Host salish
	HostName salish.pgc.nrcan.gc.ca
	User <username>
	IdentityFile ~/.ssh/id_salish
	IdentitiesOnly yes


Host leo2g
	HostName leo2g.pgc.nrcan.gc.ca
	User <username>
	ProxyJump salish
	IdentityFile ~/.ssh/id_salish
	
# Personal Github
Host github.com
	HostName github.com
	User git
	IdentityFile ~/.ssh/id_github
	IdentitiesOnly yes
```

After this, just use `ssh leo2g`. To edit code/execute terminal commands on VSCode (it's much nicer), click on the very bottom left icon (two arrowheads pointing opposite directions); `leo2g` and `salish` will show up, select `leo2g`. 


### Github SSH Authentication

I highly recommend using SSH keys to connect to your github account; github no longer allows just password sign in on command line, and it's very annoying and finnicky to 'login' another way.

Here's the steps:
- Open github.com
- Click profile picture in top right
- Settings
- SSH and GPG Keys
- New SSH Key
- Paste PUBLIC SSH key generated above in 'Key' field
- Put new github public/private SSH keys in `~/.ssh/id_github` and `~/.ssh/id_github.pub`

