import { PropsWithChildren, memo } from "react"
import { BlocksType } from "@src/components/Blocks"
import { PlayCircle as StartBlockIcon, Code as ConditionBlockIcon, CheckCircle as ResultBlockIcon, LucideIcon} from "lucide-react"

const BlockIcon = ({ Icon }: { Icon: LucideIcon }) => (
  <Icon className="w-5 h-5 text-white" />
)

const BlocksConfig: Record<BlocksType, {className: {color: string, borderColor: string}, title: BlocksType, icon: JSX.Element}> = {
  start: {
    className: {
      color: "bg-blue-800",
      borderColor: "border-blue-800",
    },
    title: "start",
    icon: <BlockIcon Icon={StartBlockIcon} />
  },
  condition: {
    className: {
      color: "bg-purple-800",
      borderColor: "border-purple-800",
    },
    title: "condition",
    icon: <BlockIcon Icon={ConditionBlockIcon} />
  },
  result: {
    className: {
      color: "bg-orange-800",
      borderColor: "border-orange-800",
    },
    title: "result",
    icon: <BlockIcon Icon={ResultBlockIcon} />
  }
}

type BaseWrapperProps = PropsWithChildren<{
  blockType: BlocksType
}>

const BaseWrapper = ({ blockType, children }: BaseWrapperProps) => {
  return (
    <div
      className={`flex flex-col items-center justify-center group/container font-lato`}
    >
      <div className={`flex flex-col min-h-20 min-w-80 border-4 ${BlocksConfig[blockType].className.borderColor} rounded-sm w-60 box-border shadow-block-glow`}>
        <div className={`flex items-center p-2 w-full min-h-10 gap-4 ${BlocksConfig[blockType].className.color}`}>
          {BlocksConfig[blockType].icon}
          <p className="box-border text-lg font-semibold text-white">{BlocksConfig[blockType].title.toUpperCase()}</p>
        </div>
        <div className="flex-auto w-full p-3 bg-gray-400 min-h-10">
          {children}
        </div>
      </div>
    </div>
  )
}

export const BlockWrapper = memo(BaseWrapper)
