import { useState } from "react";
import { Search, Plus, Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function FareRules() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Fetch from API
  const fareRules: any[] = [];

  const filteredRules = fareRules.filter(
    (r) =>
      r.startStation.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.endStation.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-foreground mb-2">Fare Rules</h1>
          <p className="text-muted-foreground">Manage fare pricing rules</p>
        </div>
        <Button className="bg-gradient-accent shadow-glow">
          <Plus className="w-4 h-4 mr-2" />
          Add Fare Rule
        </Button>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Fare Rules</span>
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search by station..."
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
                <TableHead>Rule ID</TableHead>
                <TableHead>Start Station</TableHead>
                <TableHead>End Station</TableHead>
                <TableHead>Fare Type</TableHead>
                <TableHead>Fare Amount</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredRules.map((rule) => (
                <TableRow key={rule.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{rule.id}</TableCell>
                  <TableCell>{rule.startStation}</TableCell>
                  <TableCell>{rule.endStation}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{rule.fareType}</Badge>
                  </TableCell>
                  <TableCell className="font-bold text-foreground">₹{rule.fareAmount}</TableCell>
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
