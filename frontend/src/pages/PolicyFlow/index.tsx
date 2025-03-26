import PolicyService from "@src/services/Policy"
import { useCallback, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import ReactFlow, {
	Background,
	BackgroundVariant,
	Edge,
	Node,
	ReactFlowProvider,
	useEdgesState,
	useNodesState,
	useReactFlow,
	Connection,
	addEdge,
	ConnectionMode,
	Controls,
} from "reactflow"
import { generateUniqueNodeId } from "@src/utils/policy"
import { blockTypeToBlock } from "@src/components/Blocks"
import { edgeTypeToEdge } from "@src/components/Edges"
import { addEndMarker } from "@src/components/Edges/utils"
import Toolbar from "@src/components/Toolbar"
import { buildNodesAndEdgesFromPolicy } from "@src/utils/policy"

const initialNodes: Node[] = [
	{
		id: generateUniqueNodeId(),
		type: "start",
		position: { x: 0, y: 0 },
		data: {}
	}
]

const initialEdges: Edge[] = []

function Flow() {
	const { id } = useParams()
	const { fitView } = useReactFlow()
	const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
	const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
	const [connectionLineStyle, setConnectionLineStyle] = useState({})
	const [isDataLoaded, setIsDataLoaded] = useState(false)


	const onConnect = useCallback((newConnection: Connection) => {
		// Prevent a block from connecting to itself
		if(newConnection.source !== newConnection.target){
			return setEdges(edges => addEdge(addEndMarker(newConnection), edges))
		}
	}, [])

	const onConnectStart = useCallback(
    () => {
        setConnectionLineStyle({
          strokeWidth: 3, 
          stroke: '#000', 
          strokeOpacity: 0.8, 
          transition: 'stroke 0.2s ease-in-out',
        })
    }, []
  )

  useEffect(() => {
    const fetchPolicy = async () => {
      const policy = await PolicyService.getPolicyById(Number(id))
      if (policy.flow.length > 0) {
        const { nodes, edges } = buildNodesAndEdgesFromPolicy(policy)
        setNodes(nodes)
        setEdges(edges)
        setIsDataLoaded(true)
      }
    }
    fetchPolicy()
  }, [id])

	// Automatically adjust the view to fit the content when the page loads for the first time
  useEffect(() => {
    if (!isDataLoaded) return

    const retryFit = () => {
      setTimeout(() => {
        const success = fitView({ padding: 0.2, duration: 500 })
        if (!success) retryFit()
      }, 100)
    }

    retryFit()
  }, [isDataLoaded])

	return (
		<div className="w-full h-full overflow-hidden">
				<ReactFlow
					nodeTypes={blockTypeToBlock}
					edgeTypes={edgeTypeToEdge}
					defaultEdgeOptions={{
						type: "arrow"
					}}
					nodes={nodes}
					edges={edges}
					onNodesChange={onNodesChange}
					onEdgesChange={onEdgesChange}
					onConnect={onConnect}
					onConnectStart={onConnectStart}
					connectionMode={ConnectionMode.Strict}
					connectionLineStyle={connectionLineStyle}
					fitView
				>
					<Controls />
					<Background
						color="#ccc"
						variant={BackgroundVariant.Dots}
						size={3}
						gap={12}
					/>
				</ReactFlow>
				<Toolbar />
		</div>
	)
}

export function FlowEditor() {
	return (
		<ReactFlowProvider>
			<Flow />
		</ReactFlowProvider>
	)
}