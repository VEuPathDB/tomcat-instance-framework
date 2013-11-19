<%-- 
This dummy ROOT directory is provide to workaround an issue
where tomcat returns '400 No Host matches server name'
in response to requests for non-existant contexts
--%>
<%= application.getServerInfo() %> 
<%= java.net.InetAddress.getLocalHost().getHostName() %>

<h1 align='left'><%= System.getProperty("instance.name") %></h1>
<p>
<h2><a href='manager/html'>Manager</a></h2>

<hr>

<%-- much of this is lifted from axis/happyaxis.jsp --%>
<h2>Examining System Properties</h2>
<%
    /**
     * Dump the system properties
     */
    java.util.Enumeration props = null;
    try {
        props = System.getProperties().propertyNames();
    } catch (SecurityException se) {
    }
    if(props != null) {
        out.write("<pre>");
        for (;props.hasMoreElements();) {
            String key = (String) props.nextElement();
            out.write(key + "=" + System.getProperty(key)+"\n");
        }
        out.write("</pre><p>");
    } else {
        out.write("System properties are not accessible.");
    }
%>

<h2>Examining System Environment</h2>
<%
    java.util.Map<String, String> env = null;
    try {
        env = System.getenv();
    } catch (SecurityException se) {
    }
    if(env != null) {
        out.write("<pre>");
        for (String envName : env.keySet()) {
            out.write(envName + "=" + env.get(envName)+"\n");
        }
        out.write("</pre><p>");
    } else {
        out.write("System environment is not accessible.");
    }
  
%>
