set -eu

TARGET_DIR=$1

echo "Overwrite original files?"
select OVRWR in "yes" "no"; do
    case $OVRWR in
        yes) DEST=$TARGET_DIR; break;;
        no) read -p "destinaton?: " DEST; break;;
    esac
done

mkdir -p $DEST

for FILE in `ls $TARGET_DIR`
do
    echo "process '${TARGET_DIR}/${FILE}' ==> '${DEST}/${FILE}'..."
    python escape_xml.py escape ${TARGET_DIR}/${FILE} > ${DEST}/${FILE}
done
