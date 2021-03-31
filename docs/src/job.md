# Mitto Plugin ReqRes - Jobs

## Job Configuration

If mitto-plugin-reqres provides one or more Mitto jobs, this page should be the
root of the documentation for the job(s).  Minimally, each job should be docuemted via
its JSON Schema rendered using the `.. pydantic::` reST directive.

If `reqres.types.JobConfig` was a Pydantic class
specifying the job's JSON configuration, the following would insert the JSON Schema
documentation at this point:

```
.. pydantic:: reqres.types.JobConfig
```

Note that the above is a `reST` command that is supported by the `M2R` Markdown
processor.

See the NetSuite connector documentation for a working example.
