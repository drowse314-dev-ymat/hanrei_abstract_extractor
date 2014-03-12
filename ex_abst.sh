set -eu

# Usage:
# sh ex_abst.sh target_dir store_dir [options]

TARGET_DIR=$1
shift
STORE_DIR=$1
shift
IFS="
"

echo "# test all files first..."
for FILE in `ls $TARGET_DIR`
do
    echo "==> test ${TARGET_DIR}/${FILE}..."
    EXTR=`python ./extract.py abstract ${TARGET_DIR}/${FILE} $@`
    echo "ok."
done

mkdir -p ${STORE_DIR}

echo "# store into ${STORE_DIR}..."
for FILE in `ls $TARGET_DIR`
do
    echo "==> process ${TARGET_DIR}/${FILE}..."

    for EXTR in `python ./extract.py abstract ${TARGET_DIR}/${FILE} $@`
    do
        DATEHEADER=`echo $EXTR | sed -e "s/\(.*\)&&.*/\1/g"`
        CATABSTRACT=`echo $EXTR | sed -e "s/.*&&\(.*\)/\1/g"`
        ABSTRACT=`echo $CATABSTRACT | tr "|" "\n"`
        CATEGORY=`echo $FILE | cut -f2 -d "_"`

        mkdir -p ${STORE_DIR}/${CATEGORY}

        MODIFIER=1
        OUTPATH="${STORE_DIR}/${CATEGORY}/${CATEGORY}.${DATEHEADER}.${MODIFIER}.txt"
        while [ -f $OUTPATH ]
        do
            MODIFIER=`expr ${MODIFIER} + 1`
            OUTPATH="${STORE_DIR}/${CATEGORY}/${CATEGORY}.${DATEHEADER}.${MODIFIER}.txt"
        done

        printf "%b\n" $ABSTRACT > $OUTPATH
        echo "==> saved to ${OUTPATH}..."
    done
    echo "done."
done
