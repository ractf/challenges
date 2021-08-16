package uk.co.ractf.coffeemachine;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.tree.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLClassLoader;

public class RejectingClassLoader extends URLClassLoader {

    private static final String[] ALLOWED = new String[]{
            "java/lang",
            "java/io/PrintStream",
    };

    private static final String[] DENIED = new String[]{
            "java/lang/reflect",
            "java/lang/ClassLoader",
            "java/lang/Thread",
            "java/lang/System",
            "java/lang/SecurityManager",
            "java/lang/Runtime",
            "java/lang/ProcessBuilder",
            "java/lang/Process",
    };

    public RejectingClassLoader(final URL[] urls, final ClassLoader parent) {
        super(urls, parent);
    }

    public Class<?> findClass(String name) throws ClassNotFoundException {
        String resourcePath = name.replace('.', '/').concat(".class");
        URL classResource = findResource(resourcePath);
        byte[] data;
        try (InputStream classStream = classResource.openStream()) {
            data = readBytes(classStream);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        ClassReader classReader = new ClassReader(data);
        ClassNode classNode = new ClassNode();
        classReader.accept(classNode, ClassReader.EXPAND_FRAMES);
        for (final MethodNode method : classNode.methods) {
            for (final AbstractInsnNode instruction : method.instructions) {
                if (instruction.getType() == 6) {
                    throw new IllegalStateException("Forbidden opcode used: invokedynamic");
                }
                if (instruction instanceof MethodInsnNode) {
                    String methodOwner = ((MethodInsnNode) instruction).owner;
                    boolean allowed = !methodOwner.contains("/");
                    for (final String allow : ALLOWED) {
                        if (methodOwner.startsWith(allow)) {
                            allowed = true;
                            break;
                        }
                    }
                    for (final String deny : DENIED) {
                        if (methodOwner.startsWith(deny)) {
                            allowed = false;
                            break;
                        }
                    }
                    if (!allowed) {
                        throw new IllegalStateException("Forbidden method calls used." + methodOwner + "#" + method.name);
                    }
                }
            }
        }

        return defineClass(name, data, 0, data.length);
    }


    private byte[] readBytes(InputStream in) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int read;

        while ((read = in.read(buf)) != -1) {
            out.write(buf, 0, read);
        }

        return out.toByteArray();
    }


}
