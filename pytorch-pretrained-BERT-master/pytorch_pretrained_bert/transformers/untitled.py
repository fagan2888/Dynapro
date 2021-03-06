outputs = self.bert(input_ids[:,i].clone(), attention_mask=attention_mask[:,i].clone(),token_type_ids=token_type_ids[:,i].clone())
sequence_output = outputs[0]
sequence_list.append(sequence_output)
start_logits = self.start_score(sequence_output.contiguous().view(-1, self.sequence_length, self.bert_hidden_size)).squeeze(-1)
end_logits = self.end_score(sequence_output.contiguous().view(-1, self.sequence_length, self.bert_hidden_size)).squeeze(-1)                
before_state_start_logits = self.start_score_before(sequence_output.contiguous().view(-1, self.sequence_length, self.bert_hidden_size)).squeeze(-1)
before_state_end_logits = self.end_score_before(sequence_output.contiguous().view(-1, self.sequence_length, self.bert_hidden_size)).squeeze(-1)               
lstm_out_switch, self.hidden = self.lstm_for_tagging(sequence_output, self.hidden)
lstm_out_switch = self.ReLU(lstm_out_switch)
switch_logits = self.hidden2tag(lstm_out_switch.contiguous().view(-1, 2*self.sequence_length*self.hidden_dim))
before_state_switch_logits = self.hidden2tag_before_state(lstm_out_switch.contiguous().view(-1, 2*self.sequence_length*self.hidden_dim))
start_probs = self.softmax(start_logits)           
end_probs = self.softmax(end_logits)
switch_probs = self.softmax(switch_logits)
before_state_start_probs = self.softmax(before_state_start_logits)
before_state_end_probs = self.softmax(before_state_end_logits)
before_state_switch_probs = self.softmax(before_state_switch_logits)
start_logits_list.append(start_probs)
end_logits_list.append(end_probs)
switch_logits_list.append(switch_probs)
before_state_start_logits_list.append(before_state_start_probs)
before_state_end_logits_list.append(before_state_end_probs)
before_state_switch_logits_list.append(before_state_switch_probs)
