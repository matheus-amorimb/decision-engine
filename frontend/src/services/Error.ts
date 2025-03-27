import { AxiosError } from "axios"

type ConfigBackendApi = {
  error: string
}

type ConfigBackendiErrorMessages = "policy_not_found" | "variable_in_decision_is_missing"

const apiErrorToFrontMessage: Record<ConfigBackendiErrorMessages, string> = {
  policy_not_found: "Sorry! We couldn't found the policy request",
  variable_in_decision_is_missing: "A required variable in the decision process is missing.",
}

class ErrorService {
    static handleApiError(error: unknown): never {

      if (error instanceof AxiosError) {
        if (this.isFlowValidationError(error)) {
          this.handleFlowValidationErrors(error.response?.data?.error)
        }
  
        const apiError = error.response?.data?.error
        if (apiError && apiErrorToFrontMessage[apiError as ConfigBackendiErrorMessages]) {
          throw new Error(apiErrorToFrontMessage[apiError as ConfigBackendiErrorMessages])
        }
  
        throw new Error(this.getHttpErrorMessage(error))
      }
  
      throw new Error("An unexpected error occurred. Please try again.")
    }

    private static getHttpErrorMessage(error: AxiosError): string {
      if (!error.response) {
        return "Network error. Please check your connection."
      }
  
      switch (error.response.status) {
        case 400:
          return "Invalid request. Please check your input."
        case 401:
          return "Unauthorized. Please log in again."
        case 403:
          return "Access denied."
        case 404:
          return "The requested resource was not found."
        case 500:
          return "Internal server error. Please try again later."
        default:
          return "Something went wrong. Please try again."
      }
    }

    private static isFlowValidationError(error: AxiosError<ConfigBackendApi>): boolean {
      return (
        error.response?.status === 400 &&
        Array.isArray(error.response?.data?.error) &&
        error.response?.data?.error.every((e: any) => e.code && e.message)
      )
    }

    private static handleFlowValidationErrors(error: { code: string, message: string }[]): void {
      const errorMessages = error.map((err) => `${err.message}`).join(", ")
      throw new Error(`${errorMessages}`)
    }
}

export default ErrorService


