import { Connection, MarkerType } from "reactflow";

export const addEndMarker = (edge: Connection) => ({
  ...edge,
  markerEnd: {
    type: MarkerType.ArrowClosed,
    width: 15,
    height: 15,
    color: "#000"
  }
})