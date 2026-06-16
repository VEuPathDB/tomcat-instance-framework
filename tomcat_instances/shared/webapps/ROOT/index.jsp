<%-- 
This dummy ROOT directory is provide to workaround an issue
where tomcat returns '400 No Host matches server name'
in response to requests for non-existant contexts
--%>
<%= application.getServerInfo() %> 
<%= java.net.InetAddress.getLocalHost().getHostName() %>
