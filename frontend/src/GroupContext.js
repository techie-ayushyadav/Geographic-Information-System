import { createContext, useContext } from "react";

export const GroupContext = createContext({ groupId: null });
export const useGroup = () => useContext(GroupContext);
