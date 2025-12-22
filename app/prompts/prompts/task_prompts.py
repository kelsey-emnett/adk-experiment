"""
Task descriptions and templates for resume adaptation system.
"""

TASK_PROMPTS = {
    "resume_extraction": {
        "description": """
            Extract all text content from the resume file at: {resume_path}\n
            Parse the document and return clean, structured text that includes:\n
            - Contact information\n
            - LinkedIn profile, website, and Github links\n
            - Professional summary\n
            - Work experience with ALL role names\n
            - Education\n
            - Skills\n
            - Certifications and other relevant sections
        """,
        "expected_output": "Clean, structured text containing all resume information",
    },
    "job_analysis": {
        "description": """
            Analyze the following job description:\n\n{job_content}\n\n
            Extract and structure the following information:\n
            - Job title and level\n
            - Key responsibilities\n
            - Required qualifications and skills\n
            - Preferred qualifications\n
            - Company culture indicators\n
            - Keywords that should appear in a matching resume
    """,
        "expected_output": "Detailed analysis of job requirements and keywords",
    },
    "company_role_extractor": {
        "description": """
        # CRITICAL INSTRUCTION: EXTRACT ONLY - DO NOT GENERATE OR INFER

        You are a data extraction specialist. Your ONLY job is to extract information that
        explicitly appears in the provided resume.

        ## STRICT RULES:
        1. Extract ONLY information that is explicitly stated in the source documents
        2. DO NOT infer, assume, or generate any information
        3. DO NOT use examples from the schema as real data
        4. If information is not present, leave the field empty or use an empty list
        5. Copy company names, role titles, and years EXACTLY as they appear
        6. For descriptions, use ONLY the bullet points and text that exists in the source
        7. If a person held multiple roles at the same company, create ONE CareerOutlineItem for that company with MULTIPLE Role objects in the roles list
        8. Each Role object should have its own title, role_start_year, and role_end_year
        9. The company_start_year should be the earliest role start year, and company_end_year should be the latest role end year
        10. ALL experience bullets should go in the company's experience list, not split by role

        ## SOURCE DOCUMENTS:

        ### RESUME CONTENT:
        {resume_content}

        ## YOUR TASK:
        Extract and structure the candidate's work history into the provided pydantic clients.
        For EACH company the candidate worked at, extract:
        - Company name (exact spelling from source)
        - All roles/titles held at that company (create separate Role objects for each)
        - Start and end years for each role AND for the company overall
        - Experience bullets (copy verbatim from source, do not paraphrase)

        ## EXAMPLE STRUCTURE (for reference only, NOT real data):
        If someone was "Junior Analyst" from 2018-2020 and "Senior Analyst" from 2020-2022 at "Acme Corp":
        - Create ONE CareerOutlineItem with company="Acme Corp"
        - Add TWO Role objects: [Role(title="Junior Analyst", role_start_year=2018, role_end_year=2020), Role(title="Senior Analyst", role_start_year=2020, role_end_year=2022)]
        - Set company_start_year=2018, company_end_year=2022
        - Put ALL experience bullets in the company's experience list

        ## VALIDATION:
        Before finalizing, verify that EVERY piece of information you extracted appears
        in the source documents above. If you cannot find it in the source, DO NOT include it.
        """,
        "expected_output": "A structured CareerOutline object containing ONLY information directly extracted from the provided resume content. Each company should have ONE CareerOutlineItem with multiple Role objects if the person held multiple positions there. No generated or inferred information.",
    },
    "planning": {
        "description": """
        Create a strategic plan for the resume structure based on:\n\n
        - Job Requirements:\n{job_analysis}\n\n
        - Career Outline:\n{career_outline}\n\n
        - Candidate Resume:\n{resume_content}\n\n

        Determine:\n
        1. Which sections to include (e.g., Summary, Key Accomplishments, Experience, Education, Skills, Certifications)\n
        2. The order of sections that will have the most impact\n
        3. For each section, specify:\n
           - What content to emphasize\n
           - Key themes or achievements to highlight\n
           - Approximately how much space it should take (bullets/lines)\n
        4. Which keywords and skills from the job should be emphasized\n
        5. Based on the provided structured Career Outline, determine experiences are the most impactful and should receive the most detail\n\n

        Your plan should maximize relevance to the job while staying truthful to the candidate's background.
    """,
        "expected_output": "Detailed structural plan specifying sections, order, content emphasis, and space allocation for each section",
    },
    "resume_building": {
        "description": """
            # GOAL
            Adapt the resume to the Job Description using ONLY the provided context and the Structural Plan.

            # CRITICAL LENGTH REQUIREMENT
            The ENTIRE JSON output MUST be under 3500 tokens (~2600 words).
            This means:
            - Summary: 2-3 sentences maximum (50-75 words)
            - Accomplishments: 3-5 bullets maximum (10-15 words each)
            - Experience highlights: 3-10 bullets per role maximum (15-20 words each)
            - Skills: 5-7 categories maximum (6-8 items per category)
            - Education: Minimal highlights (0-2 per degree)

            PRIORITIZE BREVITY. Use concise, punchy bullets.

            # INPUTS (AUTHORITATIVE)
            ## Career Outline:
            {career_outline}

            ## Original Resume:
            {resume_content}

            ## Job Description Analysis:
            {job_analysis}

            ## Structural Plan:
            {structure_plan}

            # TRANSFORMATION RULES
            Facts are IMMUTABLE:
            - companies, titles, dates, metrics, tools, certifications, degrees

            Language is MUTABLE:
            - wording, verbs, emphasis, ordering, framing

            You MAY:
            - rephrase existing bullets to better align with job requirements
            - mirror job description keywords when they truthfully match experience
            - emphasize relevant aspects of existing roles

            You MUST NOT:
            - add new facts, tools, metrics, or responsibilities
            - invent outcomes or infer scope or numbers
            - guess missing details

            If a field is not supported by the inputs, OMIT it entirely.

            # OUTPUT (STRICT)
            Return ONLY valid JSON.
            No markdown. No explanations. No comments.
            KEEP IT CONCISE - aim for 2000-2500 words maximum in the entire JSON.


            # REQUIRED JSON FORMAT (STRUCTURE ONLY — DO NOT COPY CONTENT)
            {{
              "cv": {{
                "name": "Full name with credentials",
                "location": "City, State",
                "email": "email@example.com",
                "phone": "tel:+1-XXX-XXX-XXXX",
                "website": "https://example.com",
                "social_networks": [
                  {{ "network": "LinkedIn", "username": "username" }},
                  {{ "network": "GitHub", "username": "username" }}
                ],
                "sections": {{
                  "summary": [
                    "2–3 sentence professional summary"
                  ],
                  "accomplishments": [
                    {{ "bullet": "Action verb + outcome" }},
                    {{ "bullet": "Action verb + outcome" }}
                  ],
                  "experience": [
                    {{
                      "company": "Company Name 1",
                      "position": "Role Title",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM or present",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }},
                    {{
                      "company": "Company Name 2",
                      "position": "Most recent role title at this company",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "present",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }},
                    {{
                      "company": "Company Name 2",
                      "position": "Previous role title at this company",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }}
                  ],
                  "skills": [
                    {{ "bullet": "Category 1: Skill1, Skill2, Skill3" }},
                    {{ "bullet": "Category 2: Skill1, Skill2, Skill3" }}
                  ],
                  "education": [
                    {{
                      "institution": "University Name",
                      "area": "Field of Study",
                      "degree": "Degree Type",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM",
                      "highlights": [
                        "GPA / honors / relevant coursework"
                      ]
                    }}
                  ]
                }}
              }}
            }}

            # REQUIREMENTS
            - Include ALL roles and companies from the Career Outline.
            - Experience entries MUST be reverse chronological.
            - Multiple roles at the same company MUST be separate entries with the same company name.
            - highlights MUST be a flat array of strings (no nesting), each starting with an action verb.
            - Summary: 2–3 sentences maximum.
            - Skills: 5–8 categories maximum; technical and role-relevant only.
            - Use job keywords ONLY where they accurately reflect existing experience.
            - Follow the Structural Plan’s emphasis guidance without adding facts.
        """,
        "expected_output": "Complete resume in valid JSON format following the structural plan. Must be properly formatted JSON that can be parsed and converted to YAML.",
    },
    "review": {
        "description": """
            # TASK
            Review iteration {iteration} of the resume below.

            ## Resume JSON:
            {resume_text}

            ## Career Outline:
            {career_outline}

            # REVIEW CHECKLIST (OBJECTIVE)
            Evaluate the resume against the following criteria.

            ## JSON VALIDITY
            - Valid, parseable JSON
            - Single root object: {{ "cv": {{ ... }} }}
            - All content nested correctly under "cv" → "sections"
            - Arrays use square brackets
            - No trailing commas
            - Strings properly quoted and escaped

            ## STRUCTURE
            - Required fields present:
              - cv.name
              - cv.sections
            - Contact fields present ONLY if supported by input context
            - Sections match the Structural Plan exactly
            - Experience entries are in reverse chronological order
            - Multiple roles at the same company appear as separate entries

            ## EXPERIENCE COMPLETENESS
            - Each experience entry includes:
              company, position, start_date, end_date, highlights
            - Dates are in YYYY-MM format or "present"
            - ALL companies and roles from the Career Outline are included
            - highlights are a flat array of strings (no nesting)

            # CRITICAL LENGTH REQUIREMENT
            The ENTIRE JSON output MUST be under 3500 tokens (~2600 words).
            If the resume is too long, trim highlights, reduce bullet counts, and condense wording.
            Each bullet should be 15-20 words maximum.

            ## CONTENT QUALITY (NON-CREATIVE)
            - Highlights emphasize outcomes over duties
            - Language aligns with job requirements where factually supported
            - No invented metrics, tools, or responsibilities
            - Chronological accuracy preserved

            # OUTPUT
            - If ALL checks pass, output exactly:
              APPROVED – Resume is ready

            - Otherwise, return a BULLETED LIST of specific issues to fix.
              - Be concrete and actionable
              - Focus first on JSON or structural failures
              - Do NOT rewrite content
              - Do NOT include example text
        """,
        "expected_output": "Detailed review with specific feedback on JSON validity, proper structure, length, content, and formatting, or approval",
    },
    "edit": {
        "description": """
            # TASK
            Edit the resume JSON to resolve the issues identified in the Review and any validation errors.

            ## Feedback to address:
            {feedback}

            ## Validation Errors (if any):
            {validation_errors}

            ## Resume JSON to edit:
            {resume_text}

            # HARD CONSTRAINTS (FAIL IF VIOLATED)
            - Output MUST be valid JSON only.
            - No markdown, comments, or explanations.
            - Root object MUST be {{ "cv": {{ ... }} }}.
            - highlights MUST be a flat array of strings.
            - Experience order MUST remain reverse chronological.
            - Dates MUST NOT change unless explicitly required by validation errors.
            - TOTAL OUTPUT MUST BE UNDER 3500 TOKENS.
            - Multiple roles at the same company MUST be separate entries with the same company name as shown below.

            # FACTUAL SAFETY RULES
            - Do NOT add new companies, roles, dates, tools, certifications, or metrics.
            - Do NOT invent outcomes or infer numbers.
            - If feedback requests missing information not present in the resume, IGNORE that feedback.

            # CRITICAL LENGTH REQUIREMENT
            The ENTIRE JSON output MUST be under 3000 tokens (~2400 words).
            If the resume is too long, trim highlights, reduce bullet counts, and condense wording.
            Each bullet should be 15-20 words maximum.

            # ALLOWED EDITS
            You MAY:
            - Fix JSON syntax or schema errors.
            - Add missing REQUIRED fields if values already exist elsewhere in the resume.
            - Remove unsupported or invalid fields.
            - Rephrase existing bullets to better align with job requirements,
              using ONLY facts already present.
            - Adjust wording, verbs, and emphasis without adding new information.
            - Reduce or expand wording to meet required word count.

            You MUST NOT:
            - Add new experience entries.
            - Add new achievements or scope.
            - Add quantitative metrics unless already present.

            # STRUCTURE EXAMPLE (FORMAT ONLY)
            {{
              "cv": {{
                "name": "Full name with credentials",
                "location": "City, State",
                "email": "email@example.com",
                "phone": "tel:+1-XXX-XXX-XXXX",
                "website": "https://example.com",
                "social_networks": [
                  {{ "network": "LinkedIn", "username": "username" }},
                  {{ "network": "GitHub", "username": "username" }}
                ],
                "sections": {{
                  "summary": [
                    "2–3 sentence professional summary"
                  ],
                  "accomplishments": [
                    {{ "bullet": "Action verb + outcome" }},
                    {{ "bullet": "Action verb + outcome" }}
                  ],
                  "experience": [
                    {{
                      "company": "Company Name 1",
                      "position": "Role Title",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM or present",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }},
                    {{
                      "company": "Company Name 2",
                      "position": "Most recent role title at this company",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "present",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }},
                    {{
                      "company": "Company Name 2",
                      "position": "Previous role title at this company",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM",
                      "highlights": [
                        "Action verb + outcome",
                        "Action verb + outcome"
                      ]
                    }}
                  ],
                  "skills": [
                    {{ "bullet": "Category 1: Skill1, Skill2, Skill3" }},
                    {{ "bullet": "Category 2: Skill1, Skill2, Skill3" }}
                  ],
                  "education": [
                    {{
                      "institution": "University Name",
                      "area": "Field of Study",
                      "degree": "Degree Type",
                      "location": "City, State",
                      "start_date": "YYYY-MM",
                      "end_date": "YYYY-MM",
                      "highlights": [
                        "GPA / honors / relevant coursework"
                      ]
                    }}
                  ]
                }}
              }}
            }}

            # OUTPUT
            Return ONLY the corrected resume as valid JSON.
        """,
        "expected_output": "Complete revised resume in valid, properly structured JSON format with all feedback addressed and no markdown formatting",
    },
}
