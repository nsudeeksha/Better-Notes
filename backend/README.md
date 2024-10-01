 pip install -r requirements.txt 
 make .env

 uvicorn server:app --reload --port 8001

 curl -X 'POST' \
  'http://127.0.0.1:8001/process/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"notes": "* How do Stacks grow?\\nSince Stacks grow up (towards 0) and Heaps grow down (in positive direction), you subtract the max segment from the offset to get a negative offset and then add it to the base\\n* Segmentation\\n* Pros\\n* Stack and Heap can grow independently\\n* Heap can dynamically request more memory from OS if out of data\\n* Stack: if an offset is references outside of the legal segment, the OS can implicitly extend the stack\\n* Sparse allocation of address space\\n* Allow for different protection for different segments which allows for sharing of selected segments and read-only status of code\\n* Cons\\n* Each segment needs to be allocated contiguously\\n* Might not have enough physical memory for large segments\\n* External fragmentation\\n* Overhead associated with copying and moving memory around (which blocks processes from running)"}'