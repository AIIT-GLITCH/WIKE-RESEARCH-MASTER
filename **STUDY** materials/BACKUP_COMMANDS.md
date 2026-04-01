# LaCie 2TB Backup Commands
## External Drive: /media/buddy_ai/LaCie

---

## Current State

The drive is mounted READ-ONLY. Nothing can be written, deleted, or modified.

First backup: `WIKE_BACKUP_20260331` — 6.9 GB, contains:
- Desktop (all 109+ papers, THE_ALMIGHTY, IBM_REAL, WATER_WORKS, proofs, sims)
- AIIT-THRESI (full research environment, qutip_env, all code)
- Downloads (PDFs, master logs, Gary source code)
- Documents (personal files)
- Pictures (screenshots, wallpaper)
- Videos (screencasts)
- .claude (memory, project configs)

---

## Unlock the Drive (Read-Write)

```bash
sudo mount -o remount,rw /media/buddy_ai/LaCie
```

## Lock the Drive (Read-Only)

```bash
sudo mount -o remount,ro /media/buddy_ai/LaCie
```

## Verify It's Locked

```bash
echo "test" > /media/buddy_ai/LaCie/test.txt
```
If locked, you'll see: `Read-only file system`

---

## Update Existing Backup (Overwrites Old Copy)

Unlocks, syncs, re-locks — one command:

```bash
sudo mount -o remount,rw /media/buddy_ai/LaCie && rsync -av ~/Desktop/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/Desktop/ && rsync -av ~/AIIT-THRESI/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/AIIT-THRESI/ && rsync -av ~/Downloads/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/Downloads/ && rsync -av ~/Documents/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/Documents/ && rsync -av ~/Pictures/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/Pictures/ && rsync -av ~/Videos/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/Videos/ && rsync -av ~/.claude/ /media/buddy_ai/LaCie/WIKE_BACKUP_20260331/.claude/ && sudo mount -o remount,ro /media/buddy_ai/LaCie
```

---

## Create New Dated Backup (Old Backups Stay Untouched)

Creates a brand new folder like WIKE_BACKUP_20260401, WIKE_BACKUP_20260405, etc:

```bash
sudo mount -o remount,rw /media/buddy_ai/LaCie && BDIR=/media/buddy_ai/LaCie/WIKE_BACKUP_$(date +%Y%m%d) && mkdir -p "$BDIR" && rsync -av ~/Desktop/ "$BDIR/Desktop/" && rsync -av ~/AIIT-THRESI/ "$BDIR/AIIT-THRESI/" && rsync -av ~/Downloads/ "$BDIR/Downloads/" && rsync -av ~/Documents/ "$BDIR/Documents/" && rsync -av ~/Pictures/ "$BDIR/Pictures/" && rsync -av ~/Videos/ "$BDIR/Videos/" && rsync -av ~/.claude/ "$BDIR/.claude/" && sudo mount -o remount,ro /media/buddy_ai/LaCie && echo "BACKUP COMPLETE: $BDIR — DRIVE LOCKED"
```

---

## Double-Click Backup Script

There's a script on your Desktop called `backup_to_lacie.sh`. Double-click it (or right-click > Run as Program) to run a full new dated backup. It will ask for your password (sudo), back everything up, lock the drive, and tell you when it's done.

---

## Important Notes

- The drive is exFAT format — Unix file permissions (chmod) don't work on it
- The ONLY way to lock/unlock is mount -o remount,ro / rw (requires sudo)
- If you unplug and replug the drive, it will mount READ-WRITE again by default
- After plugging in, run: `sudo mount -o remount,ro /media/buddy_ai/LaCie` to re-lock
- The 2TB drive can hold roughly 290 full backups at 6.9 GB each
