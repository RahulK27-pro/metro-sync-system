import { useState } from "react";
import { Search, ArrowUpRight, ArrowDownLeft } from "lucide-react";
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

export default function Transactions() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Replace with actual API data
  const transactions = [
    { id: 1, type: "Recharge", amount: 500, date: "2024-03-15 09:00", cardNumber: "MC-1001", description: "Online Recharge" },
    { id: 2, type: "Deduction", amount: -35, date: "2024-03-15 10:15", cardNumber: "MC-1001", description: "Trip Fare" },
    { id: 3, type: "Recharge", amount: 250, date: "2024-03-15 11:30", cardNumber: "MC-1002", description: "Counter Recharge" },
    { id: 4, type: "Deduction", amount: -40, date: "2024-03-15 11:45", cardNumber: "MC-1002", description: "Trip Fare" },
  ];

  const filteredTransactions = transactions.filter((t) =>
    t.cardNumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-2">Transaction History</h1>
        <p className="text-muted-foreground">View all card transactions</p>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Transactions</span>
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search by card number..."
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
                <TableHead>Transaction ID</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Card Number</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Date & Time</TableHead>
                <TableHead>Description</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTransactions.map((transaction) => (
                <TableRow key={transaction.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{transaction.id}</TableCell>
                  <TableCell>
                    <Badge className={transaction.type === "Recharge" ? "bg-success text-success-foreground" : "bg-primary text-primary-foreground"}>
                      <div className="flex items-center gap-1">
                        {transaction.type === "Recharge" ? (
                          <ArrowDownLeft className="w-3 h-3" />
                        ) : (
                          <ArrowUpRight className="w-3 h-3" />
                        )}
                        {transaction.type}
                      </div>
                    </Badge>
                  </TableCell>
                  <TableCell className="font-mono">{transaction.cardNumber}</TableCell>
                  <TableCell className={`font-bold ${transaction.amount > 0 ? 'text-success' : 'text-primary'}`}>
                    {transaction.amount > 0 ? '+' : ''}₹{Math.abs(transaction.amount)}
                  </TableCell>
                  <TableCell>{transaction.date}</TableCell>
                  <TableCell className="text-muted-foreground">{transaction.description}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
