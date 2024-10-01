import logo from './logo.svg';
import React, { useState } from 'react';
import { Flex, Text, Button, Heading, Box } from '@radix-ui/themes';


function App() {
  const [file, setFile] = useState(null);
  const [notes, setNotes] = useState("");

  // Handle file input changes
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle notes input changes
  const handleNotesChange = (event) => {
    setNotes(event.target.value);
  };

  // Simulate form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("File uploaded:", file);
    console.log("Notes:", notes);
  };

  return (
    <div>
      <Flex gapX = "4" justify="center">
        <Box>
          <Heading size = "9" color="iris" align="center"> Better Notes </Heading>
        </Box>
      </Flex>
      <Flex gap = "4"  justify="center">
        <Box>
          <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          </form>
        </Box>
        <Box>
          <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Notes" onChange={handleNotesChange} />
          <Button variant="soft"> Submit </Button>
          </form>
        </Box>
      </Flex>
    </div>
  );
}

export default App;
