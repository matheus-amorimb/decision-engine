import { Plus as PlusIcon, SaveIcon } from 'lucide-react'
import { Menubar, MenubarContent, MenubarItem, MenubarMenu, MenubarSeparator, MenubarTrigger } from "@src/components/ui/menubar"
import { Node, useReactFlow } from 'reactflow'
import { BlocksType } from '@src/components/Blocks'
import { generateUniqueNodeId } from '@src/utils/policy'
import { buildPolicyFlow } from '@src/utils/policy'
import toast from 'react-hot-toast'
import PolicyService from '@src/services/Policy';
import { useParams } from 'react-router-dom'

export default function Toolbar() {
  const { getNodes, getEdges, setNodes } = useReactFlow()
  const { id: policyId } = useParams()

  const handleCreateNewBlock = (blockType: BlocksType) => {
    const nodes = getNodes()
    let newPosition = { x: -150, y: -100 }  
    
    if (nodes.length > 0) {
      const lastNode = nodes[nodes.length - 1]
      const offsetX = 500  
      newPosition = { 
        x: lastNode.position.x + offsetX , 
        y: lastNode.position.y 
      }
    }

    const newNode: Node = {
      id: generateUniqueNodeId(),
      type: blockType,
      position: newPosition,
      data: {}
    }

    setNodes(nodes => [
      ...nodes,
      newNode
    ])
  }

  const handleSaveFlow = async () => {
    try {
      const flowBlocks = buildPolicyFlow(getNodes(), getEdges())

      var updatedPolicy = {
        id: Number(policyId), 
        flow: flowBlocks
      }

      await PolicyService.updatePolicy(updatedPolicy)

      toast.success("Nice! Flow saved successfully!")

    } catch (error) {
      toast.error(error?.message || "Sorry, an unexpected error occurred :(")
      return
    } 
  }
  
  return (
    <div className="absolute z-10 flex translate-x-1/2 bg-transparent top-2 right-1/2">
      <Menubar className="flex items-center justify-between w-full p-0 border-2 border-black rounded-lg shadow-lg">
        <MenubarMenu>
          <MenubarTrigger className='hover:cursor-pointer'>
            <PlusIcon className='w-4 h-4 stroke-2' />
          </MenubarTrigger>
          <MenubarContent>
            <MenubarItem onClick={() => handleCreateNewBlock("condition")}>
              Condition Block
            </MenubarItem>
            <MenubarItem className='hover:cursor-pointer' onClick={() => handleCreateNewBlock("result")}>
              Result Block
            </MenubarItem>
          </MenubarContent>
        </MenubarMenu>
        <MenubarSeparator />
        <MenubarMenu>
          <MenubarTrigger className='hover:cursor-pointer'>
            <SaveIcon className='w-4 h-4 stroke-2' />
          </MenubarTrigger>
          <MenubarContent>
            <MenubarItem className='hover:cursor-pointer' onClick={handleSaveFlow}>Save Flow</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
    </div>
  )
}