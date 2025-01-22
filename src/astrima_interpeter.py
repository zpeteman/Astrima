def run_astrima(code):                                                                                                     
    lines = code.split('\n')  # Split the code into lines                                                                  
    variables = {}  # Store variables                                                                                      
    functions = {}  # Store function definitions                                                                           
    i = 0  # Line index for processing                                                                                     
                                                                                                                           
    while i < len(lines):                                                                                                  
        line = lines[i].strip()  # Clean up whitespace                                                                     
        if not line:                                                                                                       
            i += 1                                                                                                         
            continue                                                                                                       
                                                                                                                           
        if line.startswith("star"):                                                                                        
            # Variable declaration: star var = "value"                                                                     
            parts = line.split('=')                                                                                        
            var_name = parts[0].split()[1].strip()                                                                         
            value = parts[1].strip().strip('"')                                                                            
            try:                                                                                                           
                # Try evaluating the value as an arithmetic expression                                                    
                value = eval(value, {}, variables)                                                                         
            except:                                                                                                        
                pass  # If it fails, leave it as a string                                                                  
            variables[var_name] = value                                                                                    
                                                                                                                           
        elif line.startswith("shine"):                                                                                     
            # Print: shine "string with {placeholders}" or a variable                                                      
            parts = line.split(' ', 1)                                                                                     
            content = parts[1].strip()                                                                                     
                                                                                                                           
            if content.startswith('"') and content.endswith('"'):                                                          
                # Replace placeholders with variable values                                                                
                content = content.strip('"')                                                                               
                for var_name in variables:                                                                                 
                    placeholder = f"{{{var_name}}}"  # Placeholder format: {var_name}                                      
                    if placeholder in content:                                                                             
                        content = content.replace(placeholder, str(variables[var_name]))                                   
                print(content)                                                                                             
            elif content in variables:                                                                                     
                # If the content is a variable name, print its value                                                       
                print(variables[content])                                                                                  
            else:                                                                                                          
                print(f"Unknown variable: {content}")                                                                      
                                                                                                                           
        elif line.startswith("ask"):                                                                                       
            # Input: ask "prompt" into var_name                                                                            
            prompt_parts = line.split("into")                                                                              
            prompt = prompt_parts[0].split('ask')[1].strip().strip('"')                                                    
            var_name = prompt_parts[1].strip()                                                                             
            user_input = input(prompt + " ")  # Ask for user input                                                         
            try:                                                                                                           
                # Try converting input to a number                                                                         
                user_input = eval(user_input)                                                                              
            except:                                                                                                        
                pass                                                                                                       
            variables[var_name] = user_input                                                                               
                                                                                                                           
        elif line.startswith("orbit"):                                                                                     
            # Loop: orbit 3 { ... }                                                                                        
            parts = line.split()                                                                                           
            count = int(parts[1])  # Number of iterations                                                                  
            loop_body = []                                                                                                 
            i += 1                                                                                                         
            while not lines[i].strip().startswith("}"):                                                                    
                loop_body.append(lines[i].strip())                                                                         
                i += 1                                                                                                     
            for _ in range(count):                                                                                         
                run_astrima("\n".join(loop_body))                                                                          
                                                                                                                           
        elif line.startswith("light") or line.startswith("dark"):                                                          
            # Conditions: light/dark var == "value" { ... }                                                                
            keyword = "light" if line.startswith("light") else "dark"                                                      
            condition = line[len(keyword):line.index("{")].strip()                                                         
            operator = "==" if "==" in condition else "!="                                                                 
            var_name, value = map(str.strip, condition.split(operator))                                                    
            value = value.strip('"')  # Remove quotes from the value                                                       
                                                                                                                           
            i += 1                                                                                                         
            condition_met = (variables.get(var_name) == value) if operator == "==" else (variables.get(var_name) != value) 
                                                                                                                           
            if (keyword == "light" and condition_met) or (keyword == "dark" and not condition_met):                        
                while not lines[i].strip().startswith("}"):                                                                
                    run_astrima(lines[i])                                                                                  
                    i += 1                                                                                                 
            else:                                                                                                          
                while not lines[i].strip().startswith("}"):                                                                
                    i += 1                                                                                                 
                                                                                                                           
        elif line.startswith("galaxy"):                                                                                    
            # Function definition: galaxy name { ... }                                                                     
            func_name = line.split()[1]                                                                                    
            func_body = []                                                                                                 
            i += 1                                                                                                         
            while not lines[i].strip().startswith("}"):                                                                    
                func_body.append(lines[i].strip())                                                                         
                i += 1                                                                                                     
            functions[func_name] = "\n".join(func_body)                                                                    
                                                                                                                           
        elif line.startswith("call"):                                                                                      
            # Call a function: call name                                                                                   
            func_name = line.split()[1]                                                                                    
            if func_name in functions:                                                                                     
                run_astrima(functions[func_name])                                                                          
            else:                                                                                                          
                print(f"Unknown function: {func_name}")                                                                    
                                                                                                                           
        elif line.startswith("rima"):                                                                                      
            # Special keyword for Rima                                                                                     
            print("Rima, you light up my universe!")                                                                       
                                                                                                                           
        else:                                                                                                              
            print(f"Unknown command: {line}")                                                                              
                                                                                                                           
        i += 1                                                                                                             
