import { FlowValidationError, PolicyDecisionProtocol, PolicyProtocol, UpdatePolicyProtocol } from "@src/protocols/policy"
import ApiService from "@src/services/Api"
import { AxiosError } from "axios"

class PolicyService {
  
  async getPolicyById(id: number): Promise<PolicyProtocol>{
    try {
      
      const response = await ApiService.get(`/policies/blocks/${id}`)
      
      return response.data as PolicyProtocol
      
    } catch (error) {
      
      console.error("Error fetching policy:", error)
      throw error
      
    }
  }

  async getAllPolicies(): Promise<PolicyProtocol[]>{
    try {
      
      const response = await ApiService.get(`/policies`)
      
      const policies = response.data as PolicyProtocol[]

      return policies

    } catch (error) {
      
      console.error("Error fetching policies:", error)
      throw error

    }
  }

  async getPolicyVariables(id: number): Promise<string[]>{
    try {
      const response = await ApiService.get(`/policies/${id}/variables`)
      
      const variables = response.data as string[]

      return variables

    } catch (error) {
      console.error("Error fetching policies:", error)
      throw error

    }
  }

  async createPolicy(name: string): Promise<PolicyProtocol>{
    try {
      const response = await ApiService.post(`/policies`, {
        name
      })
      
      const policy = response.data

      return policy

    } catch (error) {
      
      console.error("Error creating policy:", error)
      throw error
    }
  }

  async updatePolicy(policy: UpdatePolicyProtocol): Promise<PolicyProtocol>{
    try {
      const response = await ApiService.put("/policies", policy)

      return response.data

    } catch (error) {
      if (error instanceof AxiosError) {
        const validationErrors = error.response?.data as { error: FlowValidationError[] }
    
        if (validationErrors?.error?.length) {
          throw new Error(validationErrors.error.map(err => err.message).join(", "))
        }
      } 
    
      throw new Error("An unexpected error occurred")
    }
  }

  async getPolicyDecision(policyId: number, data: any): Promise<PolicyDecisionProtocol>{
    try {
      const response = await ApiService.post(`/policies/${policyId}/decision`, data)

      return response.data as PolicyDecisionProtocol

    } catch (error) {

      throw new Error("An unexpected error occurred")
    }
  }

}

export default new PolicyService()