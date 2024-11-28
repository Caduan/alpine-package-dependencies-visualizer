from apk import Package


def write_graph_to_mermaid_file(f, index, package):
    f.write("graph LR\n")

    write_package_to_mermaid_file(f, index, package, {})


def write_package_to_mermaid_file(f, index, package, visited):
    if package.name in visited:
        return

    visited[package.name] = True
    package_visited = {}

    for dependency_name in package.depends_on:
        dependency = index.get_package(dependency_name)
        
        if dependency is None:
            continue
            
        is_command = dependency_name.startswith('/')

        if isinstance(dependency, Package):
            if dependency.name in package_visited:
                continue

            package_visited[dependency.name] = True

            if is_command:
                f.write(f"  {package.name} -. {dependency_name} .-> {dependency.name}\n")
            else:
                f.write(f"  {package.name} --> {dependency.name}\n")
                write_package_to_mermaid_file(f, index, dependency, visited)
        elif isinstance(dependency, list):
            for dep in dependency:
                if dep.name in package_visited:
                    continue

                package_visited[dep.name] = True

                if is_command:
                    f.write(f"  {package.name} -. {dependency_name} .-> {dep.name}\n")
                else:
                    f.write(f"  {package.name} --> {dep.name}\n")
                    write_package_to_mermaid_file(f, index, dep, visited)
