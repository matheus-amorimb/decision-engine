import { Handle, NodeProps, Position, useReactFlow } from "reactflow"
import { BlockWrapper } from "@src/components/Blocks/BlockWrapper"
import { Trash as TrashIcon } from "lucide-react"
import { Button } from "@src/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@radix-ui/react-tooltip"
import { Input } from "@src/components/ui/input"
import toast from "react-hot-toast"

export type ResultBlockData = {
  decision_value: string
}

export function ResultBlock({ id, data, selected }: NodeProps<ResultBlockData>){
  const { setNodes, getEdges } = useReactFlow()

  const handleDeleteBlock = () => {
    const hasEdgesConnected = getEdges().find(edge => edge.target === id)
    if (hasEdgesConnected) {
      toast.error("There are blocks connected to this one. Please remove them before deleting it.")
      return
    }
    setNodes((nodes) => nodes.filter((node) => node.id !== id))
  }

  const handleInputChange = (decisionValue: string) => {
    setNodes((nodes) =>
      nodes.map((node) =>
        node.id === id
          ? { ...node, data: { ...node.data, decision_value: decisionValue } }
          : node
      )
    )
  }

  return(
    <>
      <BlockWrapper
        blockType="result"
      >
        <Input 
          type="text" 
          placeholder="Decision value" 
          className="h-12 p-2 font-bold text-center text-black uppercase bg-white border border-gray-300 rounded-md"
          value={data.decision_value}
          onChange={(event) => handleInputChange(event.target.value)}
        />
        <Handle
          type="target"
          id="target"
          position={Position.Left}
          isConnectable={true}
          isConnectableStart={false}
          className="border-orange-800 node-handle-top hover:border-orange-800"
          />
      </BlockWrapper>
      <div className="flex items-center justify-center m-6">
        {selected ?
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    className="-m-2 nodrag nopan"
                    onClick={handleDeleteBlock}
                  >
                    <TrashIcon className="w-2 h-2" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent className="p-2 text-sm text-white bg-black rounded-md shadow-lg" side="bottom" sideOffset={4}>
                  <p>Delete block</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
         : null}
      </div>
    </>
  )
}