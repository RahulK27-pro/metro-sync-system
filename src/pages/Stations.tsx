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

export default function Stations() {
  const [searchTerm, setSearchTerm] = useState("");

  // TODO: Fetch from API
  const stations: any[] = [];

  const getLineColorClass = (color: string) => {
    const colorMap: Record<string, string> = {
      Blue: "bg-blue-500",
      Red: "bg-red-500",
      Green: "bg-green-500",
      Yellow: "bg-yellow-500",
      Purple: "bg-purple-500",
    };
    return colorMap[color] || "bg-gray-500";
  };

  const filteredStations = stations.filter((s) =>
    s.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-foreground mb-2">Station Management</h1>
          <p className="text-muted-foreground">Manage metro stations and lines</p>
        </div>
        <Button className="bg-gradient-accent shadow-glow">
          <Plus className="w-4 h-4 mr-2" />
          Add Station
        </Button>
      </div>

      <Card className="shadow-md">
        <CardHeader className="border-b border-border/50">
          <CardTitle className="flex items-center justify-between">
            <span>All Stations</span>
            <div className="relative w-72">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search stations..."
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
                <TableHead>Station ID</TableHead>
                <TableHead>Station Name</TableHead>
                <TableHead>Line</TableHead>
                <TableHead>Zone</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredStations.map((station) => (
                <TableRow key={station.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-medium">{station.id}</TableCell>
                  <TableCell className="font-semibold">{station.name}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${getLineColorClass(station.lineColor)}`}></div>
                      <span>{station.lineColor} Line</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{station.zone}</Badge>
                  </TableCell>
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
