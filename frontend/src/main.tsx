import "vite-env.d.ts"
import "reactflow/dist/style.css"
import "@src/index.css"

import routes from "@src/pages/routes"
import React from "react"
import ReactDOM from "react-dom/client"
import { RouterProvider, createBrowserRouter } from "react-router-dom"
import { Toaster } from "react-hot-toast"

const router = createBrowserRouter(routes, {
  future: {
    v7_normalizeFormMethod: true,
  },
})

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
      <Toaster position="top-right"/>
        <RouterProvider router={router} future={{ v7_startTransition: true }} />
    </React.StrictMode>
)
