import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";

interface Summary {
  title: string;
  key_points: string[];
  action_items: string[];
}

interface Props {
  summary: Summary;
}

export default function SummaryCard({ summary }: Props) {
  return (
    <Card variant="outlined" sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {summary.title}
        </Typography>

        <Typography variant="subtitle1">Key Points</Typography>
        <List dense>
          {summary.key_points.map((point, idx) => (
            <ListItem key={idx}>
              <ListItemText primary={point} />
            </ListItem>
          ))}
        </List>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle1">Action Items</Typography>
        <List dense>
          {summary.action_items.map((action, idx) => (
            <ListItem key={idx}>
              <ListItemText primary={action} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}