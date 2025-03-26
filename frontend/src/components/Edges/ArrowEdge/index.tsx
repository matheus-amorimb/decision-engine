import {
  BaseEdge,
  EdgeLabelRenderer,
  EdgeProps,
  getSimpleBezierPath,
  useReactFlow,
} from 'reactflow'
import { Edge } from 'reactflow'
import { Trash as TrashIcon} from "lucide-react"
import { Button } from '@src/components/ui/button'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@radix-ui/react-tooltip'
 
export function ArrowEdge({ id, sourceX, sourceY, targetX, targetY, selected, markerEnd } : EdgeProps) {
  const { setEdges } = useReactFlow()
  const [edgePath, labelX, labelY] = getSimpleBezierPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
  })

  const handleDeleteEdge = () => {
    setEdges((edges: Edge[]) => edges.filter((edge) => edge.id !== id))
  }
 
  return (
    <>
      <BaseEdge 
        id={id} 
        path={edgePath} 
        markerEnd={markerEnd}
        style={{
          strokeWidth: 3, 
          stroke: '#000', 
          strokeDasharray: selected ? '4' : '0', 
          strokeOpacity: 0.8, 
          transition: 'stroke 0.2s ease-in-out',
        }}
      />
      { selected ? 
        <EdgeLabelRenderer>
            <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                  <Button
                    style={{
                      position: 'absolute',
                      transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
                      pointerEvents: 'all',
                    }}
                    className="nodrag nopan"
                    onClick={handleDeleteEdge}
                  >
                  <TrashIcon className="w-4 h-4" />
                </Button>
                  </TooltipTrigger>
                  <TooltipContent className="p-2 text-sm text-white bg-black rounded-md shadow-lg" side="right" sideOffset={4}>
                    <p>Delete edge</p>
                  </TooltipContent>
                </Tooltip>
            </TooltipProvider>
          </EdgeLabelRenderer> : null}
    </>
  )
}