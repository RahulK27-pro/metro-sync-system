import { useState } from "react";
import { Search, Clock } from "lucide-react";
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

export default function Trips() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Fetch from API
  const trips: any[] = [];

  const filteredTrips = trips.filter((t) =>
    t.cardNumber.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-2">Trip History</h1>
        <p className="text-muted-foreground">View all passenger trips</p>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Trips</span>
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
                <TableHead>Trip ID</TableHead>
                <TableHead>Card Number</TableHead>
                <TableHead>Entry Station</TableHead>
                <TableHead>Exit Station</TableHead>
                <TableHead>Entry Time</TableHead>
                <TableHead>Exit Time</TableHead>
                <TableHead>Fare</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTrips.map((trip) => (
                <TableRow key={trip.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{trip.id}</TableCell>
                  <TableCell className="font-mono">{trip.cardNumber}</TableCell>
                  <TableCell>{trip.entryStation}</TableCell>
                  <TableCell>{trip.exitStation}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-muted-foreground" />
                      {trip.entryTime}
                    </div>
                  </TableCell>
                  <TableCell>
                    {trip.exitTime ? (
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-muted-foreground" />
                        {trip.exitTime}
                      </div>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell className="font-semibold">
                    {trip.fareAmount > 0 ? `₹${trip.fareAmount}` : "-"}
                  </TableCell>
                  <TableCell>
                    <Badge className={trip.status === "Ongoing" ? "bg-warning text-warning-foreground" : "bg-success text-success-foreground"}>
                      {trip.status}
                    </Badge>
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
