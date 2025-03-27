import { PolicyDecisionProtocol, PolicyProtocol, UpdatePolicyProtocol } from "@src/protocols/policy"
import ApiService from "@src/services/Api"
import ErrorService from "@src/services/Error"

class PolicyService {
  
  async getPolicyById(id: number): Promise<PolicyProtocol>{
    try {
      
      const response = await ApiService.get(`/policies/blocks/${id}`)
      
      return response.data as PolicyProtocol
      
    } catch (error) {
      ErrorService.handleApiError(error)
    }
  }

  async getAllPolicies(): Promise<PolicyProtocol[]>{
    try {
      
      const response = await ApiService.get(`/policies`)
      
      const policies = response.data as PolicyProtocol[]

      return policies

    } catch (error) {
      ErrorService.handleApiError(error)
    }
  }

  async getPolicyVariables(id: number): Promise<string[]>{
    try {
      const response = await ApiService.get(`/policies/${id}/variables`)
      
      const variables = response.data as string[]

      return variables

    } catch (error) {
      ErrorService.handleApiError(error)
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
      ErrorService.handleApiError(error)
    }
  }

  async updatePolicy(policy: UpdatePolicyProtocol): Promise<PolicyProtocol>{
    try {
      const response = await ApiService.put("/policies", policy)

      return response.data

    } catch (error) {
      ErrorService.handleApiError(error)
    }
  }

  async getPolicyDecision(policyId: number, data: any): Promise<PolicyDecisionProtocol>{
    try {
      const response = await ApiService.post(`/policies/${policyId}/decision`, data)

      return response.data as PolicyDecisionProtocol

    } catch (error) {
      ErrorService.handleApiError(error)
    }
  }

}

export default new PolicyService()