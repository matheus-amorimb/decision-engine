import { Edge, Handle, NodeProps, Position, useStore } from "reactflow"
import { BlockWrapper } from "@src/components/Blocks/BlockWrapper"

export type StartBlockData = {
  title?: string
  next_block_id?: number
  next_block_temp_id?: string
}

export function StartBlock({ id, data }: NodeProps<StartBlockData>){
  const edges: Edge[] = useStore((state) => state.edges)

  var isHandleConnected = edges.some(edge => edge.source === id)
  
  return(
    <BlockWrapper
      blockType="start"
    >
      <div className="flex items-center justify-center">
      <p className="box-border text-lg font-bold tracking-wide text-white drop-shadow-md">
        {data?.title?.toUpperCase()}
      </p>
      </div>
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