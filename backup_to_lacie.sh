#!/bin/bash
# WIKE BACKUP SCRIPT — backs up everything to LaCie, locks drive read-only
# Double-click or run: bash ~/Desktop/backup_to_lacie.sh

BDIR="/media/buddy_ai/LaCie/WIKE_BACKUP_$(date +%Y%m%d)"

echo "============================================"
echo "  WIKE BACKUP TO LACIE"
echo "  Target: $BDIR"
echo "============================================"
echo ""

# Check drive is plugged in
if [ ! -d "/media/buddy_ai/LaCie" ]; then
    echo "ERROR: LaCie drive not found. Plug it in first."
    read -p "Press Enter to close..."
    exit 1
fi

# Unlock drive
echo "Unlocking drive..."
sudo mount -o remount,rw /media/buddy_ai/LaCie
if [ $? -ne 0 ]; then
    echo "ERROR: Could not unlock drive."
    read -p "Press Enter to close..."
    exit 1
fi

# Create backup directory
mkdir -p "$BDIR"

# Back up everything
echo ""
echo "Backing up Desktop..."
rsync -a ~/Desktop/ "$BDIR/Desktop/"
echo "  Done."

echo "Backing up AIIT-THRESI..."
rsync -a ~/AIIT-THRESI/ "$BDIR/AIIT-THRESI/"
echo "  Done."

echo "Backing up Downloads..."
rsync -a ~/Downloads/ "$BDIR/Downloads/"
echo "  Done."

echo "Backing up Documents..."
rsync -a ~/Documents/ "$BDIR/Documents/"
echo "  Done."

echo "Backing up Pictures..."
rsync -a ~/Pictures/ "$BDIR/Pictures/"
echo "  Done."

echo "Backing up Videos..."
rsync -a ~/Videos/ "$BDIR/Videos/"
echo "  Done."

echo "Backing up .claude config..."
rsync -a ~/.claude/ "$BDIR/.claude/"
echo "  Done."

# Lock drive
echo ""
echo "Locking drive read-only..."
sudo mount -o remount,ro /media/buddy_ai/LaCie

# Verify
echo ""
SIZE=$(du -sh "$BDIR" 2>/dev/null | cut -f1)
echo "============================================"
echo "  BACKUP COMPLETE"
echo "  Location: $BDIR"
echo "  Size: $SIZE"
echo "  Drive: LOCKED (read-only)"
echo "============================================"

read -p "Press Enter to close..."
