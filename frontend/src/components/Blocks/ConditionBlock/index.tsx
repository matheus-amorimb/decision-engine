import { Handle, NodeProps, Position, useReactFlow } from "reactflow"
import { BlockWrapper } from "@src/components/Blocks/BlockWrapper"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@radix-ui/react-tooltip"
import { Button } from "@src/components/ui/button"
import { Trash as TrashIcon, X as ElseIcon} from "lucide-react"
import { Input } from "@src/components/ui/input"
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@src/components/ui/select"
import { Card, CardDescription } from "@src/components/ui/card"
import { ConditionOperators } from "@src/protocols/policy"
import { useEffect, useState } from "react"
import toast from "react-hot-toast"

type BlockRule = {
  variableName: string
  operator: ConditionOperators
  value: string
  next_block_id?: number
  next_block_temp_id?: string
}

export type ConditionBlockData = {
  rule?: BlockRule
}

// type HandleId = "source-condition" | "source-else" 

const conditionOperators: ConditionOperators[] = ["<", "<=", "=", "!=", ">=", ">"];

export function ConditionBlock({ id, data, selected }: NodeProps<ConditionBlockData>){
  const { setNodes, getNodes, getEdges } = useReactFlow()
  const [isElseHandleConnected, setIsElseHandleConnected] = useState<boolean>(false)
  const [isConditionHandleConnected, setIsConditionHandleConnected] = useState<boolean>(false)

  const handleDeleteBlock = () => {
    const hasEdgesConnected = getEdges().find(edge => edge.target === id || edge.source === id)
    if (hasEdgesConnected) {
      toast.error("There are blocks connected to this one. Please remove them before deleting it.")
      return
    }
    setNodes((nodes) => nodes.filter((node) => node.id !== id))
  }

  const handleConditionChange = (updatedCondition: Partial<BlockRule>) => {
    setNodes((nodes) => 
      nodes.map((node) =>
        node.id === id 
          ? {...node, 
              data: { 
                ...node.data, 
                rule: {...node.data.rule, ...updatedCondition}
              } 
            }
          : node
      )
    )
  }

  useEffect(() => {
    const conditionHandle = getEdges().some(edge => edge.source === id && edge.sourceHandle === "source-condition")
    const elseHandle = getEdges().some(edge => edge.source === id && edge.sourceHandle === "source-else")

    setIsElseHandleConnected(elseHandle)
    setIsConditionHandleConnected(conditionHandle)

  }, [getEdges(), getNodes()]);

  return(
    <>
      <BlockWrapper
        blockType="condition"
      >
        <Handle
          type="target"
          id="target"
          position={Position.Left}
          isConnectable={true}
          className="node-handle-top"
        />
        <div className="flex flex-col gap-10">
          <div className="flex flex-row">
            <div className="flex flex-row justify-between gap-1">
              <Input
                value={data.rule?.variableName}
                placeholder="Variable"
                className="h-10 p-2 font-bold text-center text-black bg-white border border-gray-300 rounded-md"
                onChange={(event) => handleConditionChange({variableName: event.target.value})}
              />
              <Select
                value={data.rule?.operator}
                onValueChange={(value) => handleConditionChange({operator: value as ConditionOperators})}
              >
                <SelectTrigger
                  className="items-center h-10 font-bold text-black bg-white border border-gray-300 rounded-md"
                >
                  <SelectValue 
                    placeholder="Operator" 
                  />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>
                      Operators
                    </SelectLabel>
                    {
                      conditionOperators.map(operator => (
                        <SelectItem key={operator} value={operator}>{operator}</SelectItem>
                      ))
                    }
                  </SelectGroup>
                </SelectContent>
              </Select>
                <Input 
                  value={data.rule?.value}
                  type="number"
                  placeholder="Value"
                  className="h-10 p-2 font-bold text-center text-black bg-white border border-gray-300 
                  rounded-md appearance-none [&::-webkit-inner-spin-button]:hidden [&::-webkit-outer-spin-button]:hidden"
                  onChange={(event) => handleConditionChange({value: event.target.value})}
                />
            </div>
            <Handle
              type="source"
              id="source-condition"
              position={Position.Right}
              isConnectable={true}
              isConnectableStart={!isConditionHandleConnected}
              isConnectableEnd={!isConditionHandleConnected}
              isValidConnection={() => !isConditionHandleConnected}
              className="-my-6 border-purple-500 node-handle-bottom hover:border-purple-600"
            />
          </div>
          <div className="flex flex-row justify-end">
            <Card className="flex flex-row items-center h-10 p-2 font-bold text-center text-black bg-white border border-gray-300 rounded-md">
              <ElseIcon 
                className="w-4 h-4 mr-2 text-red-500"
                strokeWidth={3}
              />
              <CardDescription>
                If the condition is not met
              </CardDescription>
            </Card>
            <Handle
              type="source"
              id="source-else"
              position={Position.Right}
              isConnectable={true}
              isConnectableStart={!isElseHandleConnected}
              isConnectableEnd={!isElseHandleConnected}
              isValidConnection={() => !isElseHandleConnected}
              className="border-purple-500 my-14 node-handle-bottom hover:border-purple-600"
            />
          </div>
        </div>
      </BlockWrapper>
      <div className="absolute transform -translate-x-1/2 -bottom-12 left-1/2">
        {selected ?
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    className="nodrag nopan"
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