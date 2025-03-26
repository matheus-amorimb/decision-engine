import { ComponentType } from "react"
import { NodeProps } from "reactflow"
import { StartBlock } from "@src/components/Blocks/StartBlock"
import { ConditionBlock } from "@src/components/Blocks/ConditionBlock"
import { ResultBlock } from "@src/components/Blocks/ResultBlock"

export type BlocksType = 'start' | 'condition' | 'result'

export const blockTypeToBlock: Record<BlocksType, ComponentType<NodeProps>> = {
  start: StartBlock,
  condition: ConditionBlock,
  result: ResultBlock
}