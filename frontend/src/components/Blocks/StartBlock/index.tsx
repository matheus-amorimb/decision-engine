import { Edge, Handle, NodeProps, Position, useStore } from "reactflow"
import { BlockWrapper } from "@src/components/Blocks/BlockWrapper"

export type StartBlockData = {
  next_block_id?: number
  next_block_temp_id?: string
}

export function StartBlock({ id }: NodeProps<StartBlockData>){
  const edges: Edge[] = useStore((state) => state.edges)

  var isHandleConnected = edges.some(edge => edge.source === id)
  
  return(
    <BlockWrapper
      blockType="start"
    >
      <Handle
        type="source"
        id="source"
        position={Position.Right}
        isConnectable={true}
        isConnectableStart={!isHandleConnected}
        isValidConnection={() => !isHandleConnected}
        isConnectableEnd={!isHandleConnected}
        className="node-handle-bottom"
        />
    </BlockWrapper>
  )
}