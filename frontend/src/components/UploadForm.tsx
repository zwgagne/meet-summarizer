import {
    Button,
    LinearProgress,
    Alert,
    Box,
    Typography,
  } from "@mui/material";
  import { useState, ChangeEvent, FormEvent } from "react";
  import { uploadFile, startAnalysis } from "../api";
  
  interface Props {
    onUploadComplete: (submissionId: string) => void;
  }
  
  export default function UploadForm({ onUploadComplete }: Props) {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
  
    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
      setFile(e.target.files?.[0] || null);
    };
  
    const handleSubmit = async (e: FormEvent) => {
      e.preventDefault();
      if (!file) {
        setError("Please select a file.");
        return;
      }
  
      setLoading(true);
      setError(null);
  
      try {
        const { id } = await uploadFile(file);
        await startAnalysis(id);
        onUploadComplete(id);
      } catch (err) {
        setError("An error occurred during upload.");
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <input type="file" onChange={handleFileChange} />
        <Button
          type="submit"
          variant="contained"
          sx={{ mt: 2 }}
          disabled={loading}
        >
          Upload and Analyze
        </Button>
  
        {loading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress />
            <Typography variant="caption">Uploading & analysing...</Typography>
          </Box>
        )}
  
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Box>
    );
    }