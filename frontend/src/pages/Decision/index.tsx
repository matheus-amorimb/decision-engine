import { Select, SelectContent, SelectGroup, SelectLabel, SelectTrigger, SelectValue, SelectItem } from "@src/components/ui/select"
import { PolicyProtocol } from "@src/protocols/policy"
import { useEffect, useState } from "react"
import PolicyService from '@src/services/Policy'
import { Input } from "@src/components/ui/input"
import { useForm } from "react-hook-form"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@src/components/ui/form"
import { Button } from "@src/components/ui/button"
import toast from "react-hot-toast"

export default function DecisionPage() {
  const [policies, setPolicies] = useState<PolicyProtocol[]>([])
  const [policyIdSelected, setPolicyIdSelected] = useState<string>("")
  const [policyVariables, setPolicyVariables] = useState<string[]>([])
  const [policyDecision, setPolicyDecision] = useState<string | null>(null)

  const form = useForm()

  const onSubmitForm = async (values: any) => {
    try {
      const policyDecision = await PolicyService.getPolicyDecision(Number(policyIdSelected), values)
      setPolicyDecision(policyDecision.decision)

      toast.success("Success! The decision has been calculated.")
      
    } catch (error) {
      toast.error(error.message || "Oops! Something went wrong. Please try again.")
    }
  }

  const handleOnSelectPolicy = async (policyId: number) => {
    try {
      const variables = await PolicyService.getPolicyVariables(policyId)
      
      setPolicyVariables(variables)
      setPolicyDecision(null)
      
      /*
      If there are no variables, it means the policy flow consists only of a start block 
      and a result block. In this case, there are no inputs required to determine the result, 
      so we can directly fetch the decision.
      */
      if (variables.length === 0) {
        const policyDecision = await PolicyService.getPolicyDecision(Number(policyId), {})
        setPolicyDecision(policyDecision.decision)
        toast.success("Success! The decision has been calculated.")
      }

    } catch {
      toast.error("Oops! Something went wrong. Please try again.")
    }
  }

  useEffect(() => {
    form.reset(
      policyVariables.reduce((acc, variable) => {
        acc[variable] = ""
        return acc
      }, {} as Record<string, string>)
    )
  }, [policyIdSelected, form.reset, policyVariables])

  useEffect((() => {
    const fetchData = async () => {
      const policies = await PolicyService.getAllPolicies()
      if (policies) {
        setPolicies(policies)
      }
    }
    
    fetchData()
  }), [])

  return (
    <div className="flex flex-col items-center w-[75%] p-8 gap-14 bg-zinc-500">
      <div className="flex">
        <h1 className="pb-2 text-4xl font-semibold tracking-tight border-b scroll-m-20 first:mt-0">
          Take a decision
        </h1>
      </div>
      <div className="flex min-w-96">
        <div className="flex flex-col gap-10 min-h-80">
          <div className="flex flex-col gap-6">
            <div>
              <h3 className="text-2xl font-semibold tracking-tight text-zinc-50 scroll-m-20">
                Choose a Policy
              </h3>
            </div>
            <div>
              <Select
                value={policyIdSelected}
                onValueChange={(value) => {
                  setPolicyIdSelected(value)
                  handleOnSelectPolicy(Number(value))
                }}
              >
                <SelectTrigger className="font-bold bg-white min-w-96">
                  <SelectValue placeholder="Policies" className="text-black"/>
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>
                      Policies
                    </SelectLabel>
                    {
                      policies.map(policy => (
                        <SelectItem key={policy.id} value={policy.id.toString()}>{policy.name}</SelectItem>
                      ))
                    }
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>
            {
              policyVariables.length > 0 &&
              <div className="flex flex-col gap-5">
                <h3 className="text-2xl font-semibold tracking-tight text-zinc-50 scroll-m-20">
                  Fill the Fields
                </h3>
                <div className="flex flex-col gap-4 min-w-96">
                  <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmitForm)} className="space-y-4">
                      {
                        policyVariables.map((variable) => (
                          <FormField
                          name={variable}
                          rules={{ required: `${variable} is required`}}
                          key={variable}
                          render={({field}) => (
                            <FormItem>
                                <FormLabel>{variable}</FormLabel>
                                <FormControl>
                                  <Input
                                    id={`${variable}`}
                                    type="number" 
                                    className=" bg-white appearance-none [&::-webkit-inner-spin-button]:hidden [&::-webkit-outer-spin-button]:hidden"
                                    {...field}
                                  />
                                </FormControl>
                                <FormMessage/>
                            </FormItem>
                          )}
                          />
                        ))
                      }
                      <div className="flex justify-end py-6">
                        <Button type="submit">Submit</Button>
                      </div>
                    </form>
                  </Form>
                </div>
              </div>
            }
        </div>
      </div>
      {
        policyDecision && 
        <div className="flex flex-col items-center gap-4 p-6 text-white border-2 shadow-lg border-zinc-700 bg-zinc-900 rounded-xl min-w-96">
          <h2 className="text-2xl font-bold tracking-tight text-zinc-50">
            Decision
          </h2>
          <p className="text-xl font-semibold text-green-400">
            {policyDecision.toUpperCase()}
          </p>
        </div>
      }
    </div>
  )
}