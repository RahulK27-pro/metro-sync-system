import { useState } from "react";
import { Search, Plus, Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Passengers() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Fetch from API
  const passengers: any[] = [];

  const filteredPassengers = passengers.filter(
    (p) =>
      p.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-foreground mb-2">Passenger Management</h1>
          <p className="text-muted-foreground">Manage registered passengers</p>
        </div>
        <Button className="bg-gradient-accent shadow-glow">
          <Plus className="w-4 h-4 mr-2" />
          Add Passenger
        </Button>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Passengers</span>
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search by name or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead>ID</TableHead>
                <TableHead>First Name</TableHead>
                <TableHead>Last Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Registration Date</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPassengers.map((passenger) => (
                <TableRow key={passenger.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{passenger.id}</TableCell>
                  <TableCell>{passenger.firstName}</TableCell>
                  <TableCell>{passenger.lastName}</TableCell>
                  <TableCell>{passenger.email}</TableCell>
                  <TableCell>{passenger.phone}</TableCell>
                  <TableCell>{passenger.registrationDate}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button variant="destructive" size="sm">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
