import { useEffect, useState } from "react"
import PolicyService from '@src/services/Policy';
import { PolicyProtocol } from "@src/protocols/policy";
import { Card, CardHeader, CardTitle } from "@src/components/ui/card";
import { FileText as PolicyIcon, ArrowRight as LinkToPolicyIcon, PlusCircle as AddPolicyIcon} from 'lucide-react'
import { Link } from "react-router-dom";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@src/components/ui/dialog";
import { Button } from "@src/components/ui/button";
import { Label } from "@src/components/ui/label";
import { Input } from "@src/components/ui/input";
import toast from "react-hot-toast";

export function PoliciesList() {
  const [policies, setPolicies] = useState<PolicyProtocol[]>([])
  const [newPolicyName, setNewPolicyName] = useState<string>("")

  const onCreateNewPolicy = async () => {
    try {
      const newPolicy = await PolicyService.createPolicy(newPolicyName)
      
      if (newPolicy?.id) {
        window.open(`/policy/${newPolicy.id}`, "_blank")
        window.location.reload()
        setNewPolicyName("")
      }
      
    } catch (error) {
      toast.error("Oops! We couldn't create your policy. Please try again.")
    }
  }

  useEffect(() => {
    const fetchPolicies = async () => {
      const policies = await PolicyService.getAllPolicies()
      setPolicies(policies)
    }

    fetchPolicies()

  }, [])
    
  return (
    <div className="flex flex-col w-full gap-8">
      <div className="flex justify-end w-full">
          <Dialog>
            <DialogTrigger asChild>
                <Button 
                  type="button"
                  variant="default"
                  className="flex items-center gap-3 px-4 py-2 text-white transition-all duration-200 bg-blue-600 rounded-md hover:bg-blue-700"
                >
                  <AddPolicyIcon className="w-5 h-5 mr-2" />
                  Create new policy
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>New policy</DialogTitle>
                <DialogDescription>
                  Create new policy. Click create when you're done.
                </DialogDescription>
              </DialogHeader>
                <div className="grid items-center grid-cols-4 gap-4 py-4">
                  <Label htmlFor="name" className="text-right">
                    Policy Name
                  </Label>
                  <Input 
                    id="name" 
                    value={newPolicyName} 
                    className="col-span-3"
                    onChange={(event) => setNewPolicyName(event.target.value)}
                  />
                </div>
              <DialogFooter>
                <Button 
                  type="submit"
                  className={!newPolicyName ? "cursor-not-allowed" : ""}
                  onClick={onCreateNewPolicy}
                >
                  Create
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
      </div>
      <div className="flex flex-col gap-4">
        {policies.map(policy => (
          <Card key={policy.id} className="">
            <CardHeader className="flex-row justify-between">
              <div className="flex items-center gap-3 ">
                <PolicyIcon className="w-6 h-6" /> 
                <Button
                  variant="link"
                >
                  <Link
                    to={`/policy/${policy.id}`}
                    target="_blank"
                  >
                  <CardTitle>{policy.name}</CardTitle>
                  </Link>
                </Button>
              </div>
              <Button asChild variant="secondary">
                <Link
                  to={`/policy/${policy.id}`}
                  target="_blank"
                >
                  <LinkToPolicyIcon className="w-6 h-6"/>
                </Link>
              </Button>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  )
}