import HomeLayout from "@src/components/Home";
import { PoliciesList } from "@src/pages/Policies";
import { FlowEditor } from "@src/pages/PolicyFlow";
import DecisionPage from "./Decision";
import { Navigate } from "react-router-dom";

export default [
  {
    path: "*",
    element: <Navigate to="/policies" replace />,
  },
  {
    path: "/policies",
    element: ( 
      <HomeLayout>
        <PoliciesList/>
      </HomeLayout>
    )
  },
  {
    path: "/decision",
    element: (
      <HomeLayout>
        <DecisionPage/>
      </HomeLayout>
    )
  },
  {
    path: "/policy/:id",
    element: <FlowEditor />,
  }
]
