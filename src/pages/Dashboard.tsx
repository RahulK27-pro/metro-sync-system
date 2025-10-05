import { Users, CreditCard, DollarSign, Route } from "lucide-react";
import { StatCard } from "@/components/StatCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
  // TODO: Replace with actual API data
  const stats = {
    totalPassengers: 1247,
    activeCards: 983,
    totalBalance: "₹45,678",
    totalTrips: 3456,
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-2">Dashboard</h1>
        <p className="text-muted-foreground">Monitor your transport system at a glance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Passengers"
          value={stats.totalPassengers}
          icon={Users}
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Active Cards"
          value={stats.activeCards}
          icon={CreditCard}
          trend={{ value: 8, isPositive: true }}
        />
        <StatCard
          title="Total Balance"
          value={stats.totalBalance}
          icon={DollarSign}
          trend={{ value: 15, isPositive: true }}
        />
        <StatCard
          title="Total Trips"
          value={stats.totalTrips}
          icon={Route}
          trend={{ value: 23, isPositive: true }}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="shadow-md">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50">
                <div>
                  <p className="font-medium">New Passenger Registration</p>
                  <p className="text-sm text-muted-foreground">John Doe - 2 hours ago</p>
                </div>
                <div className="w-2 h-2 rounded-full bg-success"></div>
              </div>
              <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50">
                <div>
                  <p className="font-medium">Card Recharge</p>
                  <p className="text-sm text-muted-foreground">Card #1234 - ₹500 - 3 hours ago</p>
                </div>
                <div className="w-2 h-2 rounded-full bg-accent"></div>
              </div>
              <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50">
                <div>
                  <p className="font-medium">Trip Completed</p>
                  <p className="text-sm text-muted-foreground">Station A → Station B - 5 hours ago</p>
                </div>
                <div className="w-2 h-2 rounded-full bg-primary"></div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-md">
          <CardHeader>
            <CardTitle>Quick Stats</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Active Trips</span>
                <span className="font-bold text-foreground">24</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Blocked Cards</span>
                <span className="font-bold text-destructive">3</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Total Stations</span>
                <span className="font-bold text-foreground">42</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Average Fare</span>
                <span className="font-bold text-foreground">₹35</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
