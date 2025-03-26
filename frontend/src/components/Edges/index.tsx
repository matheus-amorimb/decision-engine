import { ComponentType } from "react"
import { EdgeProps } from "reactflow"
import { ArrowEdge } from "@src/components/Edges/ArrowEdge"

export type EdgesType = "arrow" 

export const edgeTypeToEdge: Record<EdgesType, ComponentType<EdgeProps>> = {
  arrow: ArrowEdge,
}