FEUT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

FABRIC_EXTS_PATH=$FABRIC_EXTS_PATH:$FEUT_PATH
FABRIC_DFG_PATH=$FABRIC_DFG_PATH:$FEUT_PATH/presets
echo "Added Basic extensions!"
