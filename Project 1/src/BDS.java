import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class BDS {

    public static void search(State initialState, State targetState) {
        Queue<State> src_queue = new LinkedList<>();
        Queue<State> dst_queue = new LinkedList<>();

        Map<String, State> src_parents = new HashMap<>();
        Map<String, State> dst_parents = new HashMap<>();

        Map<String, State> src_visited = new HashMap<>();
        Map<String, State> dst_visited = new HashMap<>();

        src_queue.add(initialState);
        src_visited.put(initialState.hash(), initialState);
        src_parents.put(initialState.hash(), null);

        dst_queue.add(targetState);
        dst_visited.put(targetState.hash(), targetState);
        dst_parents.put(targetState.hash(), null);

        while (!src_queue.isEmpty() && !dst_queue.isEmpty()) {
            bfs(src_queue, src_visited, src_parents);
            bfs(dst_queue, dst_visited, dst_parents);

            var interstate = has_intersection(src_visited, dst_visited);
            if (interstate != null) {
                result(interstate, src_parents, dst_parents);
                break;
            }
        }
    }

    private static void bfs(Queue<State> queue, Map<String, State> visited, Map<String, State> parent) {
        var current = queue.poll();
        var children = current.successor();
        for (var child: children) {
            if (!visited.containsKey(child.hash())) {
                queue.add(child);
                visited.put(child.hash(), child);
                parent.put(child.hash(), current);
            }
        }
    }

    private static State has_intersection(Map<String, State> src_visited, Map<String, State> dst_visited) {
        for (var state: src_visited.entrySet())
            if (dst_visited.containsKey(state.getKey()))
                return state.getValue();

        return null;
    }

    private static void result(State state, Map<String, State> src_pred, Map<String, State> dst_pred){
        List<State> path = new ArrayList<>();

        var current = state;
        while (current != null) {
            path.add(0, current);
            current = src_pred.get(current.hash());
        }
        current = state;
        while (current != null) {
            path.add(current);
            current = dst_pred.get(current.hash());
        }
        try {
            FileWriter myWriter = new FileWriter("BDS_Result.txt");
            System.out.println("initial state : ");
            for (var st: path) {
                if(st.getSelectedNodeId() != -1) {
                    System.out.println("selected id : " + st.getSelectedNodeId());
                }
                st.getGraph().print();

                myWriter.write(st.getSelectedNodeId()+" ,");
                myWriter.write(st.outputGenerator()+"\n");
            }
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


