import { BlocksType } from "@src/components/Blocks"

export type PolicyProtocol = {
  id: number
  name: string
  flow: BlockProtocol[]
}

export type BlockProtocol = {
  id: number
  type: BlocksType
  decision_value: string
  next_block_id: number
  next_block_rules: BlockRuleProtocol[]
  position_y: number
  position_x: number
}

export type BlockRuleProtocol = {
  variable_name: string
  operator: ConditionOperators,
  value: string,
  next_block_id: number
  next_block_temp_id: string
}

export type CreatePolicyProtocol = {
  name: string
  flow: CreateOrUpdateBlockProtocol[]
}

export type UpdatePolicyProtocol = {
  id: number
  flow: CreateOrUpdateBlockProtocol[]
}

export type CreateOrUpdateBlockProtocol = {
  id?: number
  temp_id?: string
  type: BlocksType
  decision_value?: string
  next_block_id?: number
  next_block_temp_id?: string
  next_block_rules?: CreateOrUpdateBlockRuleProtocol[]
  position_y: number
  position_x: number
}

export type CreateOrUpdateBlockRuleProtocol = {
  variable_name: string
  operator: ConditionOperators
  value: string
  next_block_id?: number
  next_block_temp_id?: string
}

export type PolicyDecisionProtocol = {
  decision: string
}

export type ConditionOperators = "<" | "<=" |  "=" | "!=" | ">=" | ">" | "else"

export type FlowValidationError = {
  code: string
  message: string
}