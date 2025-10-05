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

export default function Cards() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Fetch from API
  const cards: any[] = [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Active":
        return "bg-success text-success-foreground";
      case "Blocked":
        return "bg-destructive text-destructive-foreground";
      case "Inactive":
        return "bg-warning text-warning-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const filteredCards = cards.filter(
    (c) =>
      c.cardNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.passengerName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-foreground mb-2">Card Management</h1>
          <p className="text-muted-foreground">Manage transport cards</p>
        </div>
        <Button className="bg-gradient-accent shadow-glow">
          <Plus className="w-4 h-4 mr-2" />
          Issue New Card
        </Button>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Cards</span>
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search by card number or passenger..."
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
                <TableHead>Card ID</TableHead>
                <TableHead>Card Number</TableHead>
                <TableHead>Balance</TableHead>
                <TableHead>Issue Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Passenger</TableHead>
                <TableHead>Card Type</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredCards.map((card) => (
                <TableRow key={card.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{card.id}</TableCell>
                  <TableCell className="font-mono">{card.cardNumber}</TableCell>
                  <TableCell className="font-semibold">₹{card.balance}</TableCell>
                  <TableCell>{card.issueDate}</TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(card.status)}>{card.status}</Badge>
                  </TableCell>
                  <TableCell>{card.passengerName}</TableCell>
                  <TableCell>{card.cardType}</TableCell>
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
