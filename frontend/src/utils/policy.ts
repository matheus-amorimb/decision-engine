import { BlocksType } from "@src/components/Blocks";
import { ConditionBlockData } from "@src/components/Blocks/ConditionBlock";
import { ResultBlockData } from "@src/components/Blocks/ResultBlock";
import { StartBlockData } from "@src/components/Blocks/StartBlock";
import { BlockRuleProtocol, CreateOrUpdateBlockProtocol, CreateOrUpdateBlockRuleProtocol, PolicyProtocol } from "@src/protocols/policy";
import { nanoid } from "nanoid";
import { Node, Edge, MarkerType } from "reactflow";

export const buildPolicyFlow = (nodes: Node[], edges: Edge[]): CreateOrUpdateBlockProtocol[]  => {
  let blocks: CreateOrUpdateBlockProtocol[] = []

  nodes.forEach((node) => {
    
    if (node.type === "start") {
      const startBlock = buildStartBlockFromNode(node, edges)
      blocks.push(startBlock)
    }

    if (node.type === "result") {
      const decisionBlock = buildDecisionBlockFromNode(node)
      blocks.push(decisionBlock)
    }

    if (node.type === "condition") {
      const conditionBlock = buildConditionBlockFromNode(node, edges)
      blocks.push(conditionBlock)
    }
  })

  return blocks
}

const buildStartBlockFromNode = (node: Node<StartBlockData>, edges: Edge[]): CreateOrUpdateBlockProtocol => {
  const startBlockEdge = edges.find((edge) => edge.source === node.id)

  if (!startBlockEdge) {
    throw Error("Start block is missing connection")
  }

  const blockId = getBlockId(node.id) 
  const nextBlockId = getNextBlockId(startBlockEdge.target)

  const startBlock: CreateOrUpdateBlockProtocol = {
    ...blockId,
    ...nextBlockId,
    type: node.type as BlocksType,
    next_block_rules: [],
    position_y: node.position.y,
    position_x: node.position.x
  }

  return startBlock
}

const buildDecisionBlockFromNode = (node: Node<ResultBlockData>): CreateOrUpdateBlockProtocol => {
  const blockId = getBlockId(node.id)
  
  const decisionValue = node.data.decision_value

  if (!decisionValue) {
    throw new Error("Result block is missing decision value")
  }

  const resultBlock: CreateOrUpdateBlockProtocol = {
    ...blockId,
    type: node.type as BlocksType,
    decision_value: decisionValue,
    position_y: node.position.y,
    position_x: node.position.x
  }

  return resultBlock
}

const buildConditionBlockFromNode = (node: Node<ConditionBlockData>, edges: Edge[]): CreateOrUpdateBlockProtocol => {
  const blockId = getBlockId(node.id) 
  const rules = buildConditionRules(node, edges)

  const conditionBlock: CreateOrUpdateBlockProtocol = {
    ...blockId,
    type: node.type as BlocksType,
    next_block_rules: rules,
    position_y: node.position.y,
    position_x: node.position.x
  }

  return conditionBlock
}

const buildConditionRules = (conditionNode: Node<ConditionBlockData>, edges: Edge[]): CreateOrUpdateBlockRuleProtocol[] => {
  const variableName = conditionNode.data.rule?.variableName
  const operator = conditionNode.data.rule?.operator
  const value = conditionNode.data.rule?.value

  if (!variableName || !operator || !value) {
    throw new Error("Condition block has empty fields")
  }

  let elseNextBlockId = {}
  let conditionNextBlockId = {}
  edges.forEach((edge) => {
    if (conditionNode.id === edge.source && edge.sourceHandle === "source-condition") {
      conditionNextBlockId = getNextBlockId(edge.target)
    }
    
    if (conditionNode.id === edge.source && edge.sourceHandle === "source-else") {
      elseNextBlockId = getNextBlockId(edge.target)
    }
  })

  if (isEmptyObject(conditionNextBlockId) || isEmptyObject(elseNextBlockId)) {
    throw new Error("Condition block is missing connections")
  }

  const conditionRule: CreateOrUpdateBlockRuleProtocol = {
    variable_name: variableName!,
    operator: operator!,
    value: value!,
    ...conditionNextBlockId
  }

  const elseRule: CreateOrUpdateBlockRuleProtocol = {
    variable_name: variableName!,
    operator: "else",
    value: value!,
    ...elseNextBlockId
  }

  return [conditionRule, elseRule]
}

export const buildNodesAndEdgesFromPolicy = (policy: PolicyProtocol): { nodes: Node[], edges: Edge[]} => {
  let nodes: Node[] = []
  let edges: Edge[] = []
  let idToTempId: Record<number, string> = {}
  
  policy.flow.forEach((block) => {
    const nodePosition = { x: block.position_x, y: block.position_y }
    
    /*
      For START BLOCK:
      - Every start block has an edge.
    */
    
    if (block.type === "start") {
      let nextBlockTempId = idToTempId[block.next_block_id] || generateUniqueNodeId();

      // If the next_block_id does not already have a tempId, add it to the map
      if (!idToTempId[block.next_block_id]) {
        idToTempId[block.next_block_id] = nextBlockTempId;
      }

      // Since a start block has only one outgoing edge, there's no need to
      // check if its ID exists in the map before assigning it.
      const nodeTempId = generateUniqueNodeId()
      const startNode: Node<StartBlockData> = {
        id: nodeTempId,
        type: "start",
        position: nodePosition,
        data: {
          next_block_temp_id: nextBlockTempId
        }
      }

      const edge: Edge = {
        id: generateUniqueNodeId(),
        source: nodeTempId,
        target: nextBlockTempId,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          width: 15,
          height: 15,
          color: "#000"
        }
      }

      nodes.push(startNode)
      edges.push(edge)
    }

    if (block.type === "condition") {
      const nodeTempId = idToTempId[block.id] || generateUniqueNodeId() 

      let trueRule: BlockRuleProtocol = {
        variable_name: "",
        operator: "<",
        value: "",
        next_block_id: 0,
        next_block_temp_id: ""
      }
      block.next_block_rules.forEach((rule) => {

        let nextBlockTempId = idToTempId[rule.next_block_id] || generateUniqueNodeId()
        if (!idToTempId[rule.next_block_id]) {
          idToTempId[rule.next_block_id] = nextBlockTempId;
        }

        if (rule.operator === "else") {
          const edge: Edge = {
            id: generateUniqueNodeId(),
            source: nodeTempId,
            target: nextBlockTempId,
            sourceHandle: "source-else",
            markerEnd: {
              type: MarkerType.ArrowClosed,
              width: 15,
              height: 15,
              color: "#000"
            }
          }
          edges.push(edge)
        } else {
          trueRule = rule
          const edge: Edge = {
            id: generateUniqueNodeId(),
            source: nodeTempId,
            target: nextBlockTempId,
            sourceHandle: "source-condition",
            markerEnd: {
              type: MarkerType.ArrowClosed,
              width: 15,
              height: 15,
              color: "#000"
            }
          }
          edges.push(edge)
        }
      })

      const conditionNode: Node<ConditionBlockData> = {
        id: nodeTempId,
        type: "condition",
        position: nodePosition,
        data: {
          rule: {
            variableName: trueRule.variable_name,
            operator: trueRule.operator,
            value: trueRule.value,
            next_block_temp_id: trueRule.next_block_temp_id
          }
        }
      }

      idToTempId[block.id] = nodeTempId

      nodes.push(conditionNode)
    }
    
    if (block.type === "result") {
      const tempId = idToTempId[block.id] || generateUniqueNodeId() 
      const resultNode: Node<ResultBlockData> = {
        id: tempId,
        type: "result",
        position: nodePosition,
        data: {
          decision_value: block.decision_value
        }
      }
      
      idToTempId[block.id] = tempId

      nodes.push(resultNode)
    }
  })

  return {
    nodes,
    edges
  }
}

export const generateUniqueNodeId = () => {
  const arbitraryButShortIdLength = 10;
  return nanoid(arbitraryButShortIdLength);
}

const isOnlyDigits = (str: string): boolean => {
  return /^\d+$/.test(str);
}

const getBlockId = (id: string) => {
  return isOnlyDigits(id) ? { id: Number(id) } : { temp_id: id }
}

const getNextBlockId = (target: string) =>  {
  return isOnlyDigits(target) ? { next_block_id: Number(target) } : { next_block_temp_id: target }
}

const isEmptyObject = (obj: object): boolean => {
  return Object.keys(obj).length === 0
}
